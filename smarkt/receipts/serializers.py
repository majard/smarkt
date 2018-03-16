from rest_framework import serializers
from .models import Receipt

class ReceiptSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Receipt
        fields = ('id', 'name', 'quantity', 'owner',
        	'price', 'average_price')