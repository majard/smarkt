from django.test import TestCase

from django.urls import reverse
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer

PRODUCT_NAME = "Maçã"
ANOTHER_PRODUCT_NAME = "Biscoito"

class ProductModelTests(APITestCase):

	def test_model_can_create_products(self):
		old_count = Product.objects.count()
		Product.objects.create(name = PRODUCT_NAME)
		new_count = Product.objects.count()
		self.assertNotEqual(old_count, new_count)


class ProductViewTests(APITestCase):

	@classmethod
	def setUp(self):
		"""setup the client"""
		self.client = APIClient()
		"""Create a Product in the DB"""
		Product.objects.create(name = PRODUCT_NAME)		
		self.product = Product.objects.get()
		self.serializer = ProductSerializer(self.product)

	def test_api_can_create_a_product(self):
		payload = {'name': ANOTHER_PRODUCT_NAME}
		response = self.client.post(
			reverse('create_product'), 
			payload, format = "json"
		)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_api_can_get_a_product(self):
		"""Test the api can get a given product."""

		#render a JSON for the expected product 
		expected_response = JSONRenderer().render(self.serializer.data)

		response = self.client.get(
		    reverse('product_details', kwargs = {'pk': self.product.id}),
		    format="json"
		)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertContains(response, expected_response)

	def test_api_can_update_product(self):
		"""Test the api can update a given product."""
		change_product = {'name': ANOTHER_PRODUCT_NAME}
		response = self.client.put(
		    reverse('product_details', kwargs = {'pk': self.product.id}),
		    change_product, format="json"
		)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
	
	def test_api_can_delete_product(self):
		"""Test the api can delete a product."""
		product = Product.objects.get()
		response = self.client.delete(
		    reverse('product_details', kwargs={'pk': product.id}),
		    format='json',
		    follow=True
		)
		self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)