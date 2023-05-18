from rest_framework import serializers
from core.models import User


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "phone_number",
            "profile_img",
            "location_set",
        ]
