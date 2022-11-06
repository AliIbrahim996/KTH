from rest_framework import serializers
from core.models import Chef, Documents
from .meal_serializer import MealSerializer
from .address_serializer import ChefAddressSerializer


class DocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = ("id", "img", "type")


class ChefSerializer(serializers.ModelSerializer):
    meals_set = MealSerializer(many=True)
    address_set = ChefAddressSerializer()
    documents_set = DocumentsSerializer(many=True)

    class Meta:
        model = Chef
        fields = [
            "id",
            "full_name",
            "user_name",
            "phone_number",
            "email",
            "password",
            "address_set",
            "date_created",
            "status",
            "views",
            "meals_set",
            "documents_set",
        ]
