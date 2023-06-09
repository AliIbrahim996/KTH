from rest_framework import serializers
from core.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from phonenumber_field.serializerfields import PhoneNumberField


# Register User
class RegistrationSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all()),
        ],
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "full_name",
            "password",
            "password2",
            "phone_number",
        ]
        extra_kwargs = {
            "full_name": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            phone_number=validated_data["phone_number"],
            full_name=validated_data["full_name"],
            password=validated_data["password"],
        )
        return user


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(
        style={"input_type": "password"}, required=True
    )
    new_password = serializers.CharField(
        style={"input_type": "password"}, required=True
    )

    def validate_current_password(self, value):
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError({"current_password": "Does not match"})
        return value
