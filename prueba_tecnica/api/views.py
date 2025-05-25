from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework import status
from .utils import api_vtx
from .serializers import *
from io import BytesIO
from .models import *

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


import pandas as pd
import os

# Create your views here.
class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all().order_by('id')
    serializer_class = OrderSerializer

    def list(self, request, *args, **kwargs):

        try:
            resp = api_vtx(os.environ['URL_ORDERS'])
            if resp != "Error":
                return Response(resp, status=status.HTTP_200_OK)
        
        except:
            return Response({"error": "Error al obtener la infomación de las ordenes"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def retrieve(self, request, *args, **kwargs):
        try:
            orderId = kwargs.get('pk')
            
            if not orderId:
                return Response({"error": "El id de la orden es requerido"}, status=status.HTTP_400_BAD_REQUEST)

            url = f'{os.environ['URL_ORDER']}/{orderId}'
            resp = api_vtx(url)

            return Response(resp, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": f"Error al obtener la infomación de la orden: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=False, methods=["GET"])
    def movements(self, request, pk=None):
        try:
            params = request.query_params
            start_date = params.get('start_date')
            end_date = params.get('end_date')

            if not start_date or not end_date:
                data = self.queryset.filter().values()
            
            if start_date and end_date:
                data = self.queryset.filter(date__range=[start_date, end_date]).values()

            if start_date and not end_date:
                data = self.queryset.filter(date__gte=start_date).values()

            if not start_date and end_date:
                data = self.queryset.filter(date__lte=end_date).values()

            resp = self.composeDataMovements(data, list=True, request=request)
            return Response(resp, status=status.HTTP_200_OK)
        
        except:
            return Response({"detail" : "Error obtiniendo la información de los movimientos"}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def composeDataMovements(self, data, list=True, request=None):
        
        for item in data:
            originId = item['origin_id_id']
            destinationId = item['destination_id_id']

            origin = Warehouses.objects.get(id=originId)
            serializer_origin = WarehousesSerializer(origin)
            item['origin_id_id'] = serializer_origin.data

            destination = Destinations.objects.get(id=destinationId)
            serializer_destination = DestinationsSerializer(destination)
            item['destination_id_id'] = serializer_destination.data

        return data
    
    @action(detail=True, methods=["GET"])
    def detail_order(self, request, pk=None):
        try:
            instance = self.get_object()

            if not instance:
                return Response({"error": "El id de la orden es requerido"}, status=status.HTTP_400_BAD_REQUEST)

            data = DetailsOrder.objects.filter(order_id=instance).values()
            resp = self.composeData(data, list=True, request=request)
            return Response(resp, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": f"Error al obtener la infomación de la orden: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def composeData(self, data, list=True, request=None):
        products = []

        for item in data:
            orderId = item['order_id']
            productId = item['product_id_id']

            order = Orders.objects.get(id=orderId)
            serializer_order = OrderSerializer(order)
            item['order_id'] = serializer_order.data
            
            product = Products.objects.get(id=productId)
            serializer_product = ProductsSerializer(product)
            products.append(serializer_product.data)
            item['product_id_id'] = products

        return data[0]

class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all().order_by('id')    
    serializer_class = ProductsSerializer


    @action(detail=False, methods=["GET"])
    def specific_products(self, request, pk=None):
                
        details = DetailsOrder.objects.select_related(
        'order', 'product_id', 'order__origin_id').all()
        data = []

        for detail in details:
            warehouse = detail.order.origin_id.sla
            delivery_company = detail.order.origin_id.delivery_company
            product = detail.product_id.name
            quantity = detail.quantity
            data.append({
                'bodega': warehouse,
                'compañia de entrega': delivery_company,
                'producto': product,
                'cantidad': quantity
            })

        # print(details)
        df = pd.DataFrame(data)
        resumen = df.groupby(['bodega','producto','compañia de entrega'])['cantidad'].sum().reset_index()
        # result = resumen.to_dict(orient='records')

        result = []
        for (bodega, delivery_company), grupo in resumen.groupby(['bodega', 'compañia de entrega']):
            productos = [
                {"nombre": row['producto'], "cantidad": int(row['cantidad'])}
                for _, row in grupo.iterrows()
            ]
            result.append({
                "bodega": bodega,
                'compañia de entrega': delivery_company,
                "productos": productos
            })
            
        
        return Response(result, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["GET"])
    def specific_products_chart(self, request, pk=None): 
        try:
            details = DetailsOrder.objects.select_related(
                'order', 'product_id', 'order__origin_id').all()
            data = []
            for detail in details:
                warehouse = detail.order.origin_id.sla
                delivery_company = detail.order.origin_id.delivery_company
                product = detail.product_id.name
                quantity = detail.quantity
                data.append({
                    'bodega': warehouse,
                    'compañia de entrega': delivery_company,
                    'producto': product,
                    'cantidad': quantity
                })

            df = pd.DataFrame(data)
            resumen = df.groupby(['bodega','producto','compañia de entrega'])['cantidad'].sum().reset_index()


            # Etiquetas: "Producto (Bodega - Compañía)"
            resumen['etiqueta'] = resumen.apply(
                lambda row: f"{row['producto']} ({row['bodega']})", axis=1)
            etiquetas = resumen['etiqueta'].tolist()
            cantidades = resumen['cantidad'].tolist()

            fig, ax = plt.subplots(figsize=(12, 6))
            ax.barh(etiquetas, cantidades, color='mediumslateblue')
            ax.set_xlabel('Cantidad')
            ax.set_ylabel('Producto (Bodega)')
            ax.set_title('Cantidad de productos por bodega')
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            plt.tight_layout()

            buf = BytesIO()
            plt.savefig(buf, format='png')
            plt.close(fig)
            buf.seek(0)
            return HttpResponse(buf.getvalue(), content_type='image/png')

        except Exception as e:
            return HttpResponse(f"Error al generar la gráfica: {e}", status=500)
        
    @action(detail=False, methods=["GET"])
    def city_destination_products(self, request, pk=None):
        
        details = DetailsOrder.objects.select_related(
        'order', 'product_id', 'order__origin_id').all()
        data = []

        for detail in details:
            city = detail.order.destination_id.city
            product = detail.product_id.name
            data.append({
                'ciudad': city,
                'producto': product,
                'cantidad': detail.quantity
            })

        df = pd.DataFrame(data)
        resumen = df.groupby(['ciudad','producto'])['cantidad'].sum().reset_index()

        result = []
        for producto, grupo in resumen.groupby('producto'):
            ciudades = [
                {"ciudad": row['ciudad'], "cantidad": int(row['cantidad'])}
                for _, row in grupo.iterrows()
            ]
            result.append({
                "producto": producto,
                "ciudades": ciudades
            })

        return Response(result, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["GET"])
    def city_destination_products_chart(self, request, pk=None):
        try:
            details = DetailsOrder.objects.select_related(
                'order', 'product_id', 'order__origin_id').all()
            data = []

            for detail in details:
                city = detail.order.destination_id.city
                product = detail.product_id.name
                quantity = detail.quantity
                data.append({
                    'ciudad': city,
                    'producto': product,
                    'cantidad': quantity
                })

            import pandas as pd
            import matplotlib.pyplot as plt
            from matplotlib.ticker import MaxNLocator

            df = pd.DataFrame(data)
            # Agrupa y suma la cantidad real de productos por ciudad
            resumen = df.groupby(['producto', 'ciudad'])['cantidad'].sum().reset_index()

            # Ordena por producto y ciudad
            resumen = resumen.sort_values(by=['producto', 'ciudad'])

            # Etiquetas: "Producto (Ciudad)"
            resumen['etiqueta'] = resumen.apply(lambda row: f"{row['producto']} ({row['ciudad']})", axis=1)
            etiquetas = resumen['etiqueta'].tolist()
            cantidades = resumen['cantidad'].tolist()

            fig, ax = plt.subplots(figsize=(12, 6))
            ax.barh(etiquetas, cantidades, color='coral')
            ax.set_xlabel('Cantidad')
            ax.set_ylabel('Producto (Ciudad)')
            ax.set_title('Cantidad de cada producto enviado a cada ciudad')
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            plt.tight_layout()

            buf = BytesIO()
            plt.savefig(buf, format='png')
            plt.close(fig)
            buf.seek(0)
            return HttpResponse(buf.getvalue(), content_type='image/png')

        except Exception as e:
            return HttpResponse(f"Error al generar la gráfica: {e}", status=500)

class WarehousesViewSet(viewsets.ModelViewSet):
    queryset = Warehouses.objects.all().order_by('id')
    serializer_class = WarehousesSerializer

    @action(detail=False, methods=["GET"])
    def warehouses_city(self, request, pk=None):
        try:
            details = DetailsOrder.objects.select_related(
            'order', 'product_id', 'order__origin_id').all()
            data = []

            for detail in details:
                city = detail.order.destination_id.city
                warehouse = detail.order.origin_id.sla
                data.append({
                    'ciudad': city,
                    'bodega': warehouse,
                    'cantidad': detail.quantity
                })

            df = pd.DataFrame(data)
            resumen = df.groupby(['ciudad','bodega']).size().reset_index(name='cantidad')

            result = []
            for ciudad, grupo in resumen.groupby('ciudad'):
                bodegas = [
                    {"bodega": row['bodega']}
                    for _, row in grupo.iterrows()
                ]
                result.append({
                    "ciudad": ciudad,
                    "bodegas": bodegas
                })

            return Response(result, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": f"Error al obtener la infomación de las bodegas: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=["GET"])
    def warehouses_city_chart(self, request, pk=None):
        try:
            details = DetailsOrder.objects.select_related(
                'order', 'product_id', 'order__origin_id').all()
            
            data = []
            for detail in details:
                city = detail.order.destination_id.city
                warehouse = detail.order.origin_id.sla
                data.append({
                    'ciudad': city,
                    'bodega': warehouse,
                    'cantidad': detail.quantity
                })

            df = pd.DataFrame(data)
            resumen = df.groupby(['ciudad', 'bodega']).size().reset_index(name='cantidad')

            # Ordena por bodega y ciudad alfabéticamente
            resumen = resumen.sort_values(by=['bodega', 'ciudad'])

            # Etiquetas: "Bodega (Ciudad)"
            resumen['etiqueta'] = resumen.apply(lambda row: f"{row['bodega']} ({row['ciudad']})", axis=1)
            etiquetas = resumen['etiqueta'].tolist()
            cantidades = resumen['cantidad'].tolist()

            fig, ax = plt.subplots(figsize=(10, 6))
            ax.barh(etiquetas, cantidades, color='skyblue')
            ax.set_xlabel('Cantidad')
            ax.set_ylabel('Bodega (Ciudad)')
            ax.set_title('Envios de almacenes a cada ciudad')
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            plt.tight_layout()

            buf = BytesIO()
            plt.savefig(buf, format='png')
            plt.close(fig)
            buf.seek(0)
            return HttpResponse(buf.getvalue(), content_type='image/png')

        except Exception as e:
            return Response(f"Error al generar la gráfica: {e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)