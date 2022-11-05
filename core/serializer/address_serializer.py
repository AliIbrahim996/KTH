from rest_framework import serializers
from core.models import ChefAddress

class ChefAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChefAddress
        fields = '__all__'
