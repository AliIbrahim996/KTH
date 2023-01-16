from rest_framework import serializers
from core.models import User
from phonenumber_field.serializerfields import PhoneNumberField


class CustomerSerializer(serializers.ModelSerializer):
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
