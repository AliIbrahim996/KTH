from django.shortcuts import render, get_object_or_404
from django.http import Http404
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from core.serializer import MealSerializer
from core.models import Meal


class LatestMealList(APIView):
    def get(self, request, format=None):
        meals = Meal.objects.all()[0:5]
        serializer = MealSerializer(meals, many=True)
        return Response(serializer.data)


class ChefMealList(APIView):
    def get_object(self, chef):
        try:
            return Meal.objects.get(chef=chef)
        except Meal.DoesNotExist:
            raise Http404
    
    def get(self, request, chef, format=None):
        meals = self.get_object(chef)
        serializer = MealSerializer(meals, many=True)
        return Response(serializer.data)
