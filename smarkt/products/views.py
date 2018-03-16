from rest_framework import generics
from .serializers import ProductSerializer
from .models import Product

from django_filters import rest_framework as filters
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_condition import Or
from oauth2_provider.contrib.rest_framework import \
TokenHasReadWriteScope, TokenHasScope, OAuth2Authentication

from rest_framework.authentication import SessionAuthentication

class CreateView(generics.ListCreateAPIView):	
    """This class defines the create behavior of the rest api."""
    serializer_class = ProductSerializer

    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [Or(IsAdminUser, TokenHasReadWriteScope)]
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = '__all__'

    def perform_create(self, serializer):
        """Save the post data when creating a new product."""
        serializer.save(owner=self.request.user, quantity=0)

    def get_queryset(self):
        """This view returns the products from the currently authenticated user"""
        return Product.objects.filter(owner=self.request.user)

class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [Or(IsAdminUser, TokenHasReadWriteScope)]
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = '__all__'