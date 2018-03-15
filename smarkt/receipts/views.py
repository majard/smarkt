from rest_framework import generics
from .serializers import ReceiptSerializer
from django.shortcuts import get_object_or_404
from .models import Receipt
from products.models import Product

class CreateView(generics.ListCreateAPIView):	
    """This class defines the create behavior of the rest api."""
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new receipt."""

        request_data = self.request.data
        print("self.request.data: ")
        print(self.request.data)
        product_name = request_data['name']
        quantity = request_data['quantity']
        price = request_data['price']
        receipts = Receipt.objects.filter(name=product_name)
        product = get_object_or_404(Product, name=product_name)

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
        serializer.save(average_price = average_price)

class DetailsView(generics.RetrieveDestroyAPIView):
    """This class handles the http GET and DELETE requests."""

    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer