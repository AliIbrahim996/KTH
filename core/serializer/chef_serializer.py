from rest_framework import serializers
from core.models import Chef, User, Documents
from django.contrib.auth.password_validation import validate_password
from .document_serializer import DocumentsSerializer


# Register Chef
class ChefRegistrationSerializer(serializers.ModelSerializer):

    user = User()
    # documents_set = DocumentsSerializer()

    def __init__(self, user, instance=None, data=..., **kwargs):
        self.user = user
        super().__init__(instance, data, **kwargs)

    class Meta:
        model = Chef
        fields = [
            "loc_lat",
            "loc_lan",
            "id_card",
            # "documents_set",
        ]
        extra_kwargs = {
            "id_card": {"required": True},
        }

    def create(self, validated_data):
        # documents_data = validated_data.pop("documents_set")
        self.user.save()
        chef = Chef.objects.create(
            user=self.user,
            loc_lat=validated_data["loc_lat"],
            loc_lan=validated_data["loc_lan"],
            id_card=validated_data["id_card"],
        )
        # for document in documents_data:
        #     document = Documents.objects.create(chef=chef, **document)
        #     chef.documents_set.add(document)

        # chef.save()
        return chef
