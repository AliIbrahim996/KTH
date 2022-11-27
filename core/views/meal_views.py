from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework import permissions
from core.models import Meal, Category
from core.serializer import ListMealSerializer, ChefMealSerializer


class MealsByChefView(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ListMealSerializer
    queryset = Meal.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        chef = self.request.query_params.get('chef', None)
        if chef:
            queryset = queryset.filter(chef=chef)
        else:
            queryset = Meal.objects.none()

        return queryset


class MealsByCategoryView(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ListMealSerializer
    queryset = Meal.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs['cat_id']
        category = Category.objects.all().filter(pk=category_id)
        if category:
            queryset = queryset.filter(category=category)
        else:
            queryset = Meal.objects.none()

        return queryset


class MealsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Meal.objects.all()
    serializer_class = ListMealSerializer


class MealView(APIView):

    def post(self, request):
        if request.user.is_authenticated:
            chef = getattr(request, "user", None)

            if chef is not None:
                meal_serializer = ChefMealSerializer(chef=chef, data=request.data)
                if meal_serializer.is_valid():
                    meal_serializer.save()
                    return Response(
                        {"msg": "New Meal is created!"}, status=status.HTTP_201_CREATED
                    )
                return Response(meal_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"msg": "User is unauthorized"}, status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request, pk=None):

        chef = getattr(request, "user", None)
        if chef is not None:
            if pk:
                meals = get_object_or_404(Meal.objects.all(), pk=pk)
                meal_serializer = ListMealSerializer(meals)
                return Response(meal_serializer.data)

            meals = Meal.objects.filter(chef=chef)
            if meals:
                meal_serializer = ListMealSerializer(meals, many=True)
                return Response(meal_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"msg": "You don't have any meals"}, status=status.HTTP_204_NO_CONTENT)

        return Response({"msg": "User is unauthorized"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        saved_meal = get_object_or_404(Meal.objects.all(), pk=pk)
        data = request.data.get('meal')
        serializer = ChefMealSerializer(instance=saved_meal, data=data, partial=True)

        if serializer.is_valid(raise_exception=True):
            meal = serializer.save()
        return Response({"success": "meal '{}' updated successfully".format(meal.title)})
