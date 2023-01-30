from rest_framework import serializers
from .CustomerSerializer import CustomerSerializer
from core.models import Location, User


class LocationSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(required=False)
    phone_number = serializers.CharField(source='customer.phone_number',required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        customer = User.objects.get(pk=self.context.get("user_id"))
        self.customer = CustomerSerializer(customer)

    class Meta:
        model = Location
        fields = [
            "customer",
            "phone_number",
            "loc_lat",
            "loc_lan",
            "street",
            "city",
            "country",
            "department_number",
            "location_type",
        ]


    def get_validation_exclusions(self):
        exclusions = super(LocationSerializer, self).get_validation_exclusions()
        return exclusions + ['customer']

    def create(self, validated_data):
        location = Location.objects.create(customer=self.customer.instance,
                                           loc_lan=validated_data["loc_lan"], loc_lat=validated_data["loc_lat"])
        return location
