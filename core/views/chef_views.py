from django.shortcuts import render
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework import status
from core.serializer import ChefSerializer
from core.models import Chef


class ChefList(APIView):
    def get(self, request, format=None):
        chefs = Chef.objects.all()
        serializer = ChefSerializer(chefs, many=True)
        return Response(serializer.data)
