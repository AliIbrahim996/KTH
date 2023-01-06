from rest_framework import serializers
from core.models import User
from phonenumber_field.serializerfields import PhoneNumberField


class CustomerSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name')
    username = serializers.CharField(source='user.username')
    phone_number = PhoneNumberField(source='user.phone_number')
    email = serializers.EmailField(source='user.email')
    profile_img = serializers.ImageField(source='user.profile_img')

    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "username",
            "phone_number",
            "email",
            "profile_img",
        ]
