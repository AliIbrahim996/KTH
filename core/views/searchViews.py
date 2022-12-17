from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
from core.models import Meal, Chef
from core.serializer import ListMealSerializer, ChefListSerializer


class SearchView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    meal_serializer_class = ListMealSerializer
    chef_serializer_class = ChefListSerializer

    def get(self, request):
        search_kwargs = request.query_params.get("search_kwargs", None)
        if search_kwargs:
            meals = Meal.objects.filter(title__contains=search_kwargs)
            chefs = Chef.objects.filter(user__full_name__contains=search_kwargs)
            meals_data = self.meal_serializer_class(meals, many=True).data
            chefs_data = self.chef_serializer_class(chefs, many=True).data
            return Response({
                "chefs": chefs_data,
                "meals": meals_data
            }, status=status.HTTP_200_OK)
        return Response({"msg": "Missing search keywords param!"}, status=status.HTTP_400_BAD_REQUEST)
