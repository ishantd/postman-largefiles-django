import uuid
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=420, null=True, blank=True)
    sku = models.CharField(max_length=120, primary_key=True)
    description = models.TextField(null=True, blank=True)

class ProductAggregate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=420, null=True, blank=True)
    count = models.IntegerField(default=0)
    
class DatabaseAction(models.Model):
    name = models.CharField(max_length=420, null=True, blank=True)
    status = models.CharField(max_length=420, null=True, blank=True)
    time_started = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    time_taken = models.FloatField(null=True, blank=True)
    