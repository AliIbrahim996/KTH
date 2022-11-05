from rest_framework import serializers
from core.models import Chef, Documents
from .meal_serializer import MealSerializer
from .address_serializer import ChefAddressSerializer

class DocumentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Documents
        fields = ('id', 'img', 'type')

class ChefSerializer(serializers.ModelSerializer):
    chef_meals = MealSerializer(many=True)
    chef_address = ChefAddressSerializer()
    chef_documents = DocumentsSerializer(many=True)

    class Meta:
        model = Chef
        fields = ('id', 'full_name', 'user_name', 'phone_number', 'email', 'password', 'chef_address',
         'date_created', 'status', 'views',  'chef_meals', 'chef_documents')
