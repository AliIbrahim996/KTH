from rest_framework import serializers
from core.serializer import (CustomerSerializer, ChefListSerializer)
from core.models import Order


class OrderSerializer(serializers.ModelSerializer):
    chef = ChefListSerializer
    customer = CustomerSerializer

    class Meta:
        model = Order
        fields = [
            "chef",
            "customer",
            "ordered_date",
            "review",
            "order_items",
        ]
