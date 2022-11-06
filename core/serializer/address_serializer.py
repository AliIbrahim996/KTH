from rest_framework import serializers
from core.models import Address


class ChefAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
