from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete
from django.shortcuts import get_object_or_404

from products.models import Product
from .models import Receipt

from decimal import Decimal


@receiver(pre_save, sender=Receipt)
def save_receipt_and_update_product(sender, instance, **kwargs):
	""" Checks the product exists and updates the product quantity before saving a receipt"""
	
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
	""" Updates the quantity of the product after deleting a receipt"""
	
	receipt = instance	
	product = get_object_or_404(Product, name=receipt.name)
	quantity_deleted = Decimal(receipt.quantity)
	receipt_price = Decimal(receipt.price)
	new_quantity = (product.quantity) - quantity_deleted

	if product.average_price is not None and new_quantity > 0:
		average_price = (((product.average_price * product.quantity) -
			(receipt_price * quantity_deleted)) /
    		new_quantity)
		product.average_price = average_price

	product.quantity -= quantity_deleted
	product.save()