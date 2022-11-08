from rest_framework import serializers
from core.models import User
from .RegSerializer import RegistrationSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "full_name", "user_name", "phone_number", "email", "password"]

    def create(self, validated_data):
        user = RegistrationSerializer.create(RegistrationSerializer(), validated_data)
        user.save()
        return user
