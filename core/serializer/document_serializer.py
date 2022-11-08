from rest_framework import serializers
from core.models import Documents, Chef

class DocumentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Documents
        fields = ["img"]


# class DocumentsSerializer(serializers.ModelSerializer):

#     chef = Chef()

#     def __init__(self, chef, instance=None, data=..., **kwargs):
#         self.chef = chef
#         super().__init__(instance, data, **kwargs)

#     class Meta:
#         model = Documents
#         fields = ["img"]


#     def create(self, validated_data):
#         document = Documents.objects.create(
#             chef=self.chef,
#             img=validated_data["img"],
#         )

#         return document