from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Receipt(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField(validators = [MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2, 
    	validators=[MinValueValidator(Decimal('0.01'))])
    average_price = models.DecimalField(max_digits=10, decimal_places=2,
     									null = True, blank = True)