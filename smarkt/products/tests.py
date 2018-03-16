import datetime

from django.urls import reverse
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.utils import timezone

from rest_framework.renderers import JSONRenderer
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from oauth2_provider.models import get_application_model, AccessToken

from .models import Product
from .serializers import ProductSerializer

PRODUCT_NAME = "Maçã"
ANOTHER_PRODUCT_NAME = "Biscoito"
PASSWORD = "123456"
USERNAME = "test_user"

Application = get_application_model()

class ProductModelTests(APITestCase):

	def test_model_can_create_products(self):
		old_count = Product.objects.count()
		test_user = User.objects.create_user("test_user", "test@user.com", "123456")
		Product.objects.create(name = PRODUCT_NAME, owner = test_user)
		new_count = Product.objects.count()
		self.assertNotEqual(old_count, new_count)


class ProductViewTests(APITestCase):

	def setUp(self):
		"""setup the client"""
		self.client = APIClient()
		"""Create a Product in the DB"""

		self.test_user = User.objects.create_user(USERNAME, "test@user.com", PASSWORD)
		Product.objects.create(name = PRODUCT_NAME, owner=self.test_user)		
		self.product = Product.objects.get()
		self.serializer = ProductSerializer(self.product)


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


	def test_api_can_create_a_product(self):
		response = self.client.post(
			reverse('create_product'),
			self.payload, format = "json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_api_can_get_a_product(self):
		"""Test the api can get a given product."""

		#render a JSON for the expected product response
		expected_response = JSONRenderer().render(self.serializer.data)

		response = self.client.get(
		    reverse('product_details', kwargs = {'pk': self.product.id}),
		    format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertContains(response, expected_response)

	def test_api_can_update_product(self):
		"""Test the api can update a given product."""
		response = self.client.put(
		    reverse('product_details', kwargs = {'pk': self.product.id}),
		    self.payload, format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
	
	def test_api_can_delete_product(self):
		"""Test the api can delete a product."""
		response = self.client.delete(
		    reverse('product_details', kwargs={'pk': self.product.id}),
		    format='json',
		    follow=True)
		self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)