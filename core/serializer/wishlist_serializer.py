from rest_framework import serializers
from core.models import WishList
from core.serializer import ListMealSerializer


class WishListSerializer(serializers.ModelSerializer):
    meal = ListMealSerializer()

    class Meta:
        model = WishList
        fields = [
            "id",
            "meal",
        ]

    def create(self, validated_data):
        customer = self.context.get("customer")
        return WishList.objects.create(meal=validated_data["meal"], customer=customer)
