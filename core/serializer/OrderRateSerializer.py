from rest_framework.serializers import ModelSerializer
from core.serializer import OrderSerializer
from core.models import Order
from rest_framework import serializers


class OrderRateSerializer(ModelSerializer):
    order = OrderSerializer(required=False)
    feedback = serializers.CharField(required=False)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        order = Order.objects.get(pk=self.context.get("order_id"))
        self.order = OrderSerializer(order)

    class Meta:
        model = Order
        fields = ["order", "stars", "feedback"]

    def get_validation_exclusions(self):
        exclusions = super(OrderRateSerializer, self).get_validation_exclusions()
        return exclusions + ['order'] + ['feedback']

    def create(self, validated_data):
        validated_data["order"] = self.order.instance
        return super().create(validated_data)
