from django.core.management.base import BaseCommand
from api.models import Products, Warehouses, Destinations, Orders, DetailsOrder
from django.utils.dateparse import parse_datetime
from api.utils import api_vtx

import os, json

class Command(BaseCommand):
    help = 'Import orders and details from JSON and VTEX API'

    def handle(self, *args, **kwargs):
        
        # with open('json/list_orders.json', 'r', encoding='utf-8') as f:
        #     data = json.load(f)

        data = api_vtx(os.environ['URL_ORDERS'])

        for order in data['list']:
            order_id = order['orderId']

            url = f'{os.environ["URL_ORDER"]}/{order_id}'

            try:
                resp = api_vtx(url, timeout=10)
                if resp == "Error" or not isinstance(resp, dict):
                    self.stdout.write(self.style.WARNING(f'No se pudo obtener detalle de {order_id}'))
                    continue
                detail = resp
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Error en petición de {order_id}: {e}'))
                continue

            # 2. Destino (puedes ajustar según el JSON de detalle)
            shipping_data = detail.get('shippingData', {})
            address = shipping_data.get('address', {})
            dest, _ = Destinations.objects.get_or_create(
                city=address.get('city', ''),
                state=address.get('state', ''),
                country=address.get('country', ''),
                postal_code=address.get('postalCode', '')
            )

            # 3. Origen (Warehouse, puedes ajustar según el JSON de detalle)
            warehouse_name = ''
            sla = ''
            delivery_company = ''
            price = 0
            if shipping_data.get('logisticsInfo'):
                info = shipping_data['logisticsInfo'][0]
                sla = info.get('slas', [{}])[0].get('id', '')
                delivery_company = info.get('deliveryCompany', '')
                price = info.get('slas', [{}])[0].get('price', 0)
            warehouse, _ = Warehouses.objects.get_or_create(
                sla=sla,
                price_delivery=price,
                delivery_company=delivery_company
            )

            # Extraer totales
            totals = detail.get('totals', [])
            discount = 0
            shipping = 0
            products_price = 0
            for total in totals:
                if total.get('id') == 'Discounts':
                    discount = int(total.get('value', 0))
                elif total.get('id') == 'Shipping':
                    shipping = int(total.get('value', 0))
                elif total.get('id') == 'Items':
                    products_price = int(total.get('value', 0))

            # 4. Crear la orden
            order_obj, _ = Orders.objects.get_or_create(
                order_id=order_id,
                defaults={
                    'date': parse_datetime(order['creationDate']),
                    'origin_id': warehouse,
                    'destination_id': dest,
                    'discount': discount,
                    'shipping': shipping,
                    'products_price': products_price,
                    'total': int(order.get('totalValue', 0))
                }
            )

            # 5. Agregar productos y detalles
            for item in detail.get('items', []):
                product, _ = Products.objects.get_or_create(
                    product_id=item.get('id', ''),
                    defaults={
                        'name': item.get('name', ''),
                        'ref_id': item.get('refId', ''),
                        'price': int(item.get('price', 0)),
                        'quantity': int(item.get('quantity', 0)),
                        'Sku': int(item.get('sellerSku', 0)) if item.get('sellerSku') else 0
                    }
                )
                DetailsOrder.objects.get_or_create(
                    order=order_obj,
                    product_id=product,
                    defaults={
                        'quantity': int(item.get('quantity', 0)),
                        'price': int(item.get('price', 0))
                    }
                )
            self.stdout.write(self.style.SUCCESS(f'Orden {order_id} importada'))
