from django.test import TestCase

# Create your tests here.

from .models import Product


class ProductViewTests(TestCase):
	PRODUCT_NAME = "Maçã"
	ANOTHER_PRODUCT_NAME = "Biscoito"

    def test_product_creation(self):
    	self.client.post('/products/', {'name': PRODUCT_NAME})
    	product = Product.objects.get(id=1)

        self.assertEquals(product.name, PRODUCT_NAME)