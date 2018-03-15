from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete
from django.shortcuts import get_object_or_404

from products.models import Product
from .models import Receipt

from decimal import Decimal


@receiver(pre_save, sender=Receipt)
def save_receipt_and_update_product(sender, instance, **kwargs):
	""" Checks the product exists and updates the DB before saving a receipt"""
	
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

@receiver(post_delete, sender=Receipt)
def delete_receipt_and_update_product(sender, instance, **kwargs):
	""" Updates the product table after deleting a receipt"""
	
	receipt = instance	
	product = get_object_or_404(Product, name=receipt.name)
	quantity = Decimal(receipt.quantity)
	price = Decimal(receipt.price)

	product.quantity += quantity
	product.save()