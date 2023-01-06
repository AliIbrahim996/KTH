from rest_framework import serializers
from core.models import Subscription
from core.serializer import CustomerSerializer, ChefListSerializer


class SubscriptionSerializer(serializers.ModelSerializer):
    chef = ChefListSerializer
    customer = CustomerSerializer

    def __init__(self):
        # @todo test is required
        self.chef = ChefListSerializer(self.context.get("chef"))
        self.customer = CustomerSerializer(self.context.get("customer"))

    class Meta:
        model = Subscription
        fields = [
            "id",
            "chef",
            "customer",
        ]
