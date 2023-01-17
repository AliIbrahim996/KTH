from rest_framework import serializers
from core.models import Subscription, Chef, User


class SubscriptionSerializer(serializers.ModelSerializer):
    chef = Chef()
    customer = User()

    def __init__(self, *args, **kwargs):
        context = kwargs.pop('context')
        self.chef = Chef.objects.get(pk=context.get("chef"))
        self.customer = User.objects.get(pk=context.get("customer"))
        super().__init__(*args, **kwargs)

    class Meta:
        model = Subscription
        fields = []

    def create(self, validated_data):
        return Subscription.objects.create(customer=self.customer, chef=self.chef)
