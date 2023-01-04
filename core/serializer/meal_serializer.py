from django.db.models import Avg
from rest_framework import serializers
from core.models import Meal, Chef, WishList
from core.models.meals_rate import MealsRating


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
