from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=420, null=True, blank=True)
    sku = models.CharField(max_length=120, primary_key=True)
    description = models.TextField(null=True, blank=True)