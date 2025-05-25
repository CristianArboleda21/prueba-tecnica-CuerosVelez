from rest_framework import serializers
from .models import *

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'

class DetailsOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailsOrder
        fields = '__all__'
        
class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

class WarehousesSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Warehouses
        fields = '__all__'

class DestinationsSerializer(serializers.ModelSerializer):          
    class Meta:
        model = Destinations
        fields = '__all__'