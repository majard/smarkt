from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField(blank=True, default=0)
    average_price = models.DecimalField(max_digits=10, decimal_places=2,
     									null=True, blank=True)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        response = "name: {}\n quantity: {}\naverage_price: {}"
        return response.format(self.name, self.quantity, self.average_price)