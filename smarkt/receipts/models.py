from django.db import models

class Receipt(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    average_price = models.DecimalField(max_digits=10, decimal_places=2,
     									null = True, blank = True)