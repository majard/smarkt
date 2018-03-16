from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Receipt(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField(validators = [MinValueValidator(1)])

    product = models.ForeignKey('products.Product',
        related_name='receipts', 
        on_delete=models.CASCADE)      

    owner = models.ForeignKey('auth.User',
        related_name='receipts', 
        on_delete=models.CASCADE)     
    
    price = models.DecimalField(max_digits=10, decimal_places=2, 
    	validators=[MinValueValidator(Decimal('0.01'))])

    average_price = models.DecimalField(max_digits=10, decimal_places=2,
     									null = True, blank = True)


    def __str__(self):
        """Return a human readable representation of the model instance."""
        response = "name: {}\n quantity: {}\nprice: {}\n average_price: {} "
        return response.format(self.name, self.quantity,
        	self.price, self.average_price)