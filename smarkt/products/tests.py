from django.test import TestCase

# Create your tests here.

from .models import Product

PRODUCT_NAME = "Maçã"
ANOTHER_PRODUCT_NAME = "Biscoito"

class ProductModelTests(TestCase):

	def test_model_can_create_product(self):
		old_count = Product.objects.count()
		Product.objects.create(name = PRODUCT_NAME)
		new_count = Product.objects.count()
		self.assertNotEqual(old_count, new_count)


class ProductViewTests(TestCase):

	@classmethod
	def setUpTestData(cls):
        #Create a Product in the DB
		Product.objects.create(name = PRODUCT_NAME)

	def test_post_request_creates_product(self):
		self.client.post('/products/', {'name': ANOTHER_PRODUCT_NAME})
		product = Product.objects.get(id=2)
		self.assertEquals(product.name, ANOTHER_PRODUCT_NAME)

