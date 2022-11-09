from rest_framework import serializers
from core.models import Documents


class DocumentsSerializer(serializers.ModelSerializer):
    img = serializers.ImageField()

    class Meta:
        model = Documents
        fields = ["chef", "img"]
