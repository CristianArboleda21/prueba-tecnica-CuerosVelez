from django.db import models

# Create your models here.
class Products(models.Model):
    name: models.CharField = models.CharField(default="", max_length=100)
    product_id: models.CharField = models.CharField(default="", max_length=100)
    ref_id: models.CharField = models.CharField(default="", max_length=100)
    price: models.IntegerField = models.IntegerField(default=0)
    quantity: models.IntegerField = models.IntegerField(default=0)
    Sku: models.IntegerField = models.IntegerField(default=0)
    
class Warehouses(models.Model):
    sla: models.CharField = models.CharField(default="", max_length=100)
    price_delivery: models.IntegerField = models.IntegerField(default=0)
    delivery_company: models.CharField = models.CharField(default="", max_length=100)

class Destinations(models.Model):
    city: models.CharField = models.CharField(default="", max_length=100)
    state: models.CharField = models.CharField(default="", max_length=100)
    country: models.CharField = models.CharField(default="", max_length=100)
    postal_code: models.CharField = models.CharField(default="", max_length=100)

class Orders(models.Model):
    order_id: models.CharField = models.CharField(default="", max_length=100)
    date: models.DateField = models.DateField()
    origin_id: models.ForeignKey = models.ForeignKey(Warehouses, blank=True, on_delete=models.PROTECT)
    destination_id: models.ForeignKey = models.ForeignKey(Destinations, blank=True, on_delete=models.PROTECT)
    discount: models.IntegerField = models.IntegerField(default=0)
    shipping: models.IntegerField = models.IntegerField(default=0)
    products_price: models.IntegerField = models.IntegerField(default=0)
    total: models.IntegerField = models.IntegerField(default=0)

class DetailsOrder(models.Model):
    order: models.ForeignKey = models.ForeignKey(Orders, blank=True, on_delete=models.PROTECT)
    product_id: models.ForeignKey = models.ForeignKey(Products, blank=True, on_delete=models.PROTECT)
    quantity: models.IntegerField = models.IntegerField(default=0)
    price: models.IntegerField = models.IntegerField(default=0)