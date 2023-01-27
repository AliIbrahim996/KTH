from django.db.models import Avg
from rest_framework import serializers
from core.models import Meal, Chef, WishList
from core.models.meals_rate import MealsRating
from core.serializer import ChefListSerializer


class ChefMealSerializer(serializers.ModelSerializer):
    chef = ChefListSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        chef = Chef.objects.get(user__id=self.context.get("chef_id"))
        self.chef = ChefListSerializer(chef)

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
            "delivery_time",
            "additives",
            "allergens",
        ]

    def create(self, validated_data):
        meal = Meal.objects.create(
            chef=self.chef.instance,
            title=validated_data["title"],
            description=validated_data["description"],
            price=validated_data["price"],
            image=validated_data["image"],
            dishes_count=validated_data["dishes_count"],
            category=validated_data["category"],
            is_deleted=validated_data["is_deleted"],
            delivery_time=validated_data["delivery_time"],
        )
        return meal


class ListMealSerializer(serializers.ModelSerializer):
    chef = ChefListSerializer
    category = serializers.StringRelatedField()
    rate = serializers.SerializerMethodField('get_avg_rating')
    is_liked = serializers.SerializerMethodField('get_is_liked')

    class Meta:
        model = Meal
        fields = [
            "id",
            "chef",
            "title",
            "description",
            "price",
            "image",
            "dishes_count",
            "is_deleted",
            "category",
            "rate",
            "pre_order",
            "pickup",
            "delivery",
            "is_liked",
            "delivery_time",
            "additives",
            "allergens",
        ]

    def get_avg_rating(self, meal):
        ratings = MealsRating.objects.filter(meal=meal)
        if not ratings:
            return 0.0
        return ratings.aggregate(avg_rating=Avg('stars'))['avg_rating']

    def get_is_liked(self, meal):
        user_id = self.context.get("user_id")
        if WishList.objects.filter(meal=meal.id, customer=user_id):
            return True
        return False
