from rest_framework import serializers
from .CustomerSerializer import CustomerSerializer
from core.models import Location, User


class LocationSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        customer = User.objects.get(user__id=self.context.get("user_id"))
        self.customer = CustomerSerializer(customer)

    class Meta:
        model = Location
        fields = [
            "customer",
            "loc_lat",
            "loc_lan",
        ]

    def create(self, validated_data):
        location = Location.objects.create(customer=self.customer.instance,
                                           loc_lan=validated_data["loc_lan"], loc_lat=validated_data["loc_lat"])
        return location
