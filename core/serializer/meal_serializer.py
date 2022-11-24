from rest_framework import serializers
from core.models import Meal, Chef

class ChefMealSerializer(serializers.ModelSerializer):
    chef = Chef()

    def __init__(self, chef, instance=None, data=..., **kwargs):
        self.chef = chef
        super().__init__(instance, data, **kwargs)

    class Meta:
        model = Meal
        fields = [
            "title",
            "description",
            "price",
            "image",
            "dishes_count",
            "is_deleted",
            "category",
        ]

    def create(self, validated_data):
        meal = Meal.objects.create(
            chef=self.chef,
            title=validated_data["title"],
            description=validated_data["description"],
            price=validated_data["price"],
            image=validated_data["image"],
            dishes_count=validated_data["dishes_count"],
            category=validated_data["category"],
            is_deleted=validated_data["is_deleted"],
        )
        return meal

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.image = validated_data.get('author_id', instance.image)
        instance.dishes_count = validated_data.get('author_id', instance.dishes_count)
        instance.is_deleted = validated_data.get('author_id', instance.is_deleted)

        instance.save()
        return 
        
    
class ListMealSerializer(serializers.ModelSerializer):

    chef = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    class Meta:
        model = Meal
        fields = [
            "chef",
            "title",
            "description",
            "price",
            "image",
            "dishes_count",
            "is_deleted",
            "category",
        ]