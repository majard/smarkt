from rest_framework import generics
from .serializers import ProductSerializer
from .models import Product

class CreateView(generics.ListCreateAPIView):	
    """This class defines the create behavior of the rest api."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new product."""
        serializer.save()