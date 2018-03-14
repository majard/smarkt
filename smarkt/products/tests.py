from django.test import TestCase

# Create your tests here.

from .models import Product

PRODUCT_NAME = "Maçã"
ANOTHER_PRODUCT_NAME = "Biscoito"

class ProductViewTests(TestCase):

	@classmethod
	def setUpTestData(cls):
        #Create a Product in the DB
		Product.objects.create(name = PRODUCT_NAME)

	def test_product_creation(self):
		self.client.post('/products/', {'name': PRODUCT_NAME})
		product = Product.objects.get(id=1)
		self.assertEquals(product.name, PRODUCT_NAME)