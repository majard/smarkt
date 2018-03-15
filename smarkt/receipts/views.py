from rest_framework import generics
from .serializers import ReceiptSerializer
from .models import Receipt

class CreateView(generics.ListCreateAPIView):	
    """This class defines the create behavior of the rest api."""
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new receipt."""

        serializer.save()

class DetailsView(generics.RetrieveDestroyAPIView):
    """This class handles the http GET and DELETE requests."""

    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer