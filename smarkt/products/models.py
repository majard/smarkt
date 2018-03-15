from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField(blank=True, default=0)
    average_price = models.DecimalField(max_digits=10, decimal_places=2,
     									null=True, blank=True)