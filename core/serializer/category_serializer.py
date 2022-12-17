from rest_framework import serializers
from core.models import Category
from core.serializer import ListMealSerializer


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "icon",
        ]


class ChefCategorySerializer(serializers.ModelSerializer):

    meal_set = ListMealSerializer(many=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "meal_set",
        ]
