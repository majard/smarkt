from django.db.models.signals import pre_save
from django.dispatch import receiver

from products.models import Product
from decimal import Decimal

from .models import Receipt

from django.shortcuts import get_object_or_404

@receiver(pre_save, sender=Receipt)
def save_receipt(sender, instance, **kwargs):
	
	receipt = instance	
	product = get_object_or_404(Product, name=receipt.name)
	quantity = Decimal(receipt.quantity)
	price = Decimal(receipt.price)

	if product.average_price is None:
		average_price =  price
		product.average_price = price
	else:
		average_price = (((price * quantity) + 
    		(product.average_price * product.quantity)) /
    		(quantity + product.quantity))
		product.average_price = average_price

	product.quantity += quantity
	product.save()
	receipt.average_price = average_price