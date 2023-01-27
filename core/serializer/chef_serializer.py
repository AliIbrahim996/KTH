from rest_framework import serializers
from core.models import Chef, User, Meal, Subscription
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


class SimpleMealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = [
            "id",
            "image",
        ]


class ChefListSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name')
    username = serializers.CharField(source='user.username')
    phone_number = PhoneNumberField(source='user.phone_number')
    email = serializers.EmailField(source='user.email')
    profile_img = serializers.ImageField(source='user.profile_img')
    meals_set = SimpleMealSerializer(many=True)
    followers = serializers.SerializerMethodField('get_followers')
    is_followed = serializers.SerializerMethodField('get_is_followed')

    class Meta:
        model = Chef
        fields = [
            "id",
            "full_name",
            "username",
            "phone_number",
            "bio",
            "description",
            "is_online",
            "email",
            "loc_lat",
            "loc_lan",
            "profile_img",
            "heart_number",
            "delivery_cost",
            "meals_set",
            "followers",
            "is_followed",
        ]

    def get_followers(self, obj):
        try:
            followers = Subscription.objects.filter(chef=obj.id).count()
        except Subscription.DoesNotExist:
            followers = 0
        return followers

    def get_is_followed(self, obj):
        user_id = self.context.get("user_id")
        if Subscription.objects.filter(chef=obj.id, customer=user_id):
            return True
        return False
