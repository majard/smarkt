from rest_framework import serializers
from .models import Product

class ReceiptSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Product
        fields = ('id', 'name', 'quantity', 'price', 'average_price')