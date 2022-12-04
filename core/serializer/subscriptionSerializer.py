from rest_framework import serializers
from core.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = {
            "id",
            "chef",
            "customer",
        }

    def create(self, validated_data):
        return Subscription.objects.create(chef=validated_data["chef"], customer=validated_data["customer"])
