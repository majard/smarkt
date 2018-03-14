from django.test import TestCase

from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Product

PRODUCT_NAME = "Maçã"
ANOTHER_PRODUCT_NAME = "Biscoito"

class ProductModelTests(TestCase):

	def test_model_can_create_products(self):
		old_count = Product.objects.count()
		Product.objects.create(name = PRODUCT_NAME)
		new_count = Product.objects.count()
		self.assertNotEqual(old_count, new_count)


class ProductViewTests(TestCase):

	@classmethod
	def setUp(self):
		self.client = APIClient()
        #Create a Product in the DB
		Product.objects.create(name = PRODUCT_NAME)

	def test_api_can_create_products(self):
		response = self.client.post(
			reverse('create_product'), 
			{'name': ANOTHER_PRODUCT_NAME},
			format = "json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
