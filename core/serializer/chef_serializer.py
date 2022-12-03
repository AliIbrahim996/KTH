from rest_framework import serializers
from core.models import Chef, User
from phonenumber_field.serializerfields import PhoneNumberField


# Register Chef
class ChefRegistrationSerializer(serializers.ModelSerializer):

    user = User()

    def __init__(self, user, instance=None, data=..., **kwargs):
        self.user = user
        super().__init__(instance, data, **kwargs)

    class Meta:
        model = Chef
        fields = [
            "loc_lat",
            "loc_lan",
            "id_card",
        ]
        extra_kwargs = {
            "id_card": {"required": True},
        }

    def create(self, validated_data):

        self.user.save()
        chef = Chef.objects.create(
            user=self.user,
            loc_lat=validated_data["loc_lat"],
            loc_lan=validated_data["loc_lan"],
            id_card=validated_data["id_card"],
        )

        return chef


class ChefListSerializer(serializers.ModelSerializer):

    full_name = serializers.CharField(source='user.full_name')
    user_name = serializers.CharField(source='user.user_name')
    phone_number = PhoneNumberField(source='user.phone_number')
    email = serializers.EmailField(source='user.email')
    profile_img = serializers.ImageField(source='user.profile_img')

    class Meta:
        model = Chef
        fields = [
            "id",
            "full_name",
            "user_name",
            "phone_number",
            "email",
            "loc_lat",
            "loc_lan",
            "profile_img",
            "heart_number",
        ]
