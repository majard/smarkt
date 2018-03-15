from django.urls import reverse
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from .models import Receipt
from products.models import Product
from .serializers import ReceiptSerializer
from decimal import Decimal

PRODUCT_NAME = "Maçã"
ANOTHER_PRODUCT_NAME = "Biscoito"
QUANTITY = 10
ANOTHER_QUANTITY = 20
PRICE = 2.20
ANOTHER_PRICE = 2.60

class ReceiptModelTests(APITestCase):

	def test_model_can_create_receipts(self):
		old_count = Receipt.objects.count()
		Receipt.objects.create(name = PRODUCT_NAME, quantity = QUANTITY,
			price = PRICE)
		new_count = Receipt.objects.count()
		self.assertNotEqual(old_count, new_count)


class ReceiptViewTests(APITestCase):

	@classmethod
	def setUp(self):
		"""setup the client"""
		self.client = APIClient()
		Product.objects.create(name = PRODUCT_NAME)
		Receipt.objects.create(name = PRODUCT_NAME, quantity = QUANTITY,
			price = PRICE)
		self.receipt = Receipt.objects.get()
		print(Product.objects.get())
		self.serializer = ReceiptSerializer(self.receipt)

	def test_api_can_create_a_receipt(self):
		total_sum = (PRICE * QUANTITY) + (ANOTHER_PRICE * ANOTHER_QUANTITY)
		total_quantity = QUANTITY + ANOTHER_QUANTITY
		expected_average_price = Decimal(total_sum / total_quantity)
		self.payload = {'name': PRODUCT_NAME, 'quantity': QUANTITY,
			'price' : PRICE}
		response = self.client.post(
			reverse('create_receipt'), 
			self.payload, format = "json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response.data['average_price'], expected_average_price)

	def test_api_can_get_a_receipt(self):
		"""Test the api can get a given receipt."""

		#render a JSON for the expected receipt response
		expected_response = JSONRenderer().render(self.serializer.data)

		response = self.client.get(
		    reverse('receipt_details', kwargs = {'pk': self.receipt.id}),
		    format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertContains(response, expected_response)
	
	def test_api_can_delete_receipt(self):
		"""Test the api can delete a receipt."""
		response = self.client.delete(
		    reverse('receipt_details', kwargs={'pk': self.receipt.id}),
		    format='json',
		    follow=True)
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)