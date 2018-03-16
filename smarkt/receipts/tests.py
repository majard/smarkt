import datetime

from django.urls import reverse
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.utils import timezone

from rest_framework.renderers import JSONRenderer
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from oauth2_provider.models import get_application_model, AccessToken

from .models import Receipt
from products.models import Product
from .serializers import ReceiptSerializer
from decimal import *

PRODUCT_NAME = "Maçã"
ANOTHER_PRODUCT_NAME = "Biscoito"
QUANTITY = Decimal(10)
ANOTHER_QUANTITY = Decimal(20)
PRICE = Decimal(2.20)
ANOTHER_PRICE = Decimal(2.50)
PASSWORD = "123456"
USERNAME = "test_user"

Application = get_application_model()

class ReceiptModelTests(APITestCase):

	def test_model_can_create_receipts(self):
		test_user = User.objects.create_user("test_user", "test@user.com", "123456")
		Product.objects.create(name = PRODUCT_NAME, owner = test_user)
		old_count = Receipt.objects.count()
		Receipt.objects.create(name = PRODUCT_NAME, 
			quantity = QUANTITY, price = PRICE, owner = test_user)

		new_count = Receipt.objects.count()
		self.assertNotEqual(old_count, new_count)


class ReceiptViewTests(APITestCase):

	def setUp(self):

		"""setup the client"""
		self.client = APIClient()
		"""Create a Product in the DB"""

		self.test_user = User.objects.create_user(USERNAME, "test@user.com", PASSWORD)

		self.client.login(username=USERNAME, password=PASSWORD)

		self.application = Application(
			name="Test Application",
			redirect_uris="http://localhost",
			user=self.test_user,
			client_type=Application.CLIENT_CONFIDENTIAL,
			authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
		)
		self.application.save()

		self.access_token = AccessToken.objects.create(
			user=self.test_user, token='1234567890',
			application=self.application, scope='read write',
			expires=timezone.now() + datetime.timedelta(days=1))

		self.auth_headers = 'Bearer {}'.format(self.access_token.token)

		self.payload = {'name': ANOTHER_PRODUCT_NAME}

		self.client.credentials(HTTP_AUTHORIZATION = self.auth_headers)

		#set precision for Decimals
		getcontext().prec = 2

		Product.objects.create(name = PRODUCT_NAME, owner=self.test_user)		
		self.product = Product.objects.get()

		self.receipt = Receipt.objects.create(name = PRODUCT_NAME, quantity = QUANTITY,
			owner = self.test_user, price = PRICE)

		self.serializer = ReceiptSerializer(self.receipt)
		

	def test_api_can_create_a_receipt(self):
		total_sum = (PRICE * QUANTITY) + (ANOTHER_PRICE * ANOTHER_QUANTITY)
		total_quantity = QUANTITY + ANOTHER_QUANTITY
		expected_average_price = Decimal(total_sum) / Decimal(total_quantity)

		self.payload = {'name': PRODUCT_NAME, 'quantity': ANOTHER_QUANTITY,
			'price' : ANOTHER_PRICE}
		response = self.client.post(
			reverse('create_receipt'), 
			self.payload, format = "json")

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Decimal(response.data['average_price']), expected_average_price)

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
		# create another receipt in the DB to have quantity > 0 
		Receipt.objects.create(name = PRODUCT_NAME, quantity = QUANTITY,
			price = PRICE, owner = self.test_user)
		product = Product.objects.get()
		old_quantity =  product.quantity
		old_average_price = Decimal(product.average_price)
		response = self.client.delete(
		    reverse('receipt_details', kwargs={'pk': self.receipt.id}),
		    format='json',
		    follow=True)

		# get updated object
		product.refresh_from_db()
		new_quantity = Decimal(product.quantity)
		old_sum = (old_quantity * old_average_price)
		new_average_price = old_quantity - new_quantity
		expected_average_price = (( old_sum -
			(self.receipt.price * self.receipt.quantity)) / new_quantity)

		self.assertEqual(new_average_price, self.receipt.quantity)
		self.assertEqual(product.average_price, expected_average_price)
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)