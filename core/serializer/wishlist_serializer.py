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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # We pass the "upper serializer" context to the "nested one"
        self.fields['meal'].context.update(self.context)
