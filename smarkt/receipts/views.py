from rest_framework import generics
from .serializers import ReceiptSerializer
from .models import Receipt

from django_filters import rest_framework as filters
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_condition import Or
from oauth2_provider.contrib.rest_framework import \
TokenHasReadWriteScope, TokenHasScope, OAuth2Authentication

from rest_framework.authentication import SessionAuthentication

class CreateView(generics.ListCreateAPIView):	
	"""This class defines the create behavior of the rest api."""
	serializer_class = ReceiptSerializer

	authentication_classes = [OAuth2Authentication, SessionAuthentication]
	permission_classes = [Or(IsAdminUser, TokenHasReadWriteScope)]
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = '__all__'

	def perform_create(self, serializer):
		"""Save the post data when creating a new receipt."""
		serializer.save(owner=self.request.user)

	def get_queryset(self):
		"""This view returns the products from the currently authenticated user"""
		return Receipt.objects.filter(owner=self.request.user)

class DetailsView(generics.RetrieveDestroyAPIView):
	"""This class handles the http GET and DELETE requests."""
	queryset = Receipt.objects.all()
	serializer_class = ReceiptSerializer

	authentication_classes = [OAuth2Authentication, SessionAuthentication]
	permission_classes = [Or(IsAdminUser, TokenHasReadWriteScope)]
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = '__all__'