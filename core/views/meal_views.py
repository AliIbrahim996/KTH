from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework import permissions
from core.models import Meal, Category, Chef, User
from core.serializer import ListMealSerializer, ChefMealSerializer


class MealsByChefView(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ListMealSerializer

    def get_serializer_context(self):
        context = super(MealsByChefView, self).get_serializer_context()
        context.update({"user_id": self.request.user.id})
        return context

    def get_queryset(self):
        chef_id = self.kwargs['chef_id']
        chef = Chef.objects.filter(id=chef_id)
        if chef:
            queryset = Meal.objects.filter(chef=chef_id)
        else:
            queryset = Meal.objects.none()

        return queryset


class MealsByCategoryView(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ListMealSerializer

    def get_serializer_context(self):
        context = super(MealsByCategoryView, self).get_serializer_context()
        context.update({"user_id": self.request.user.id})
        return context

    def get_queryset(self):
        category_id = self.kwargs['cat_id']
        category = Category.objects.filter(id=category_id)
        if category:
            queryset = Meal.objects.filter(category=category_id)
        else:
            queryset = Meal.objects.none()

        return queryset


class MealsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Meal.objects.all()
    serializer_class = ListMealSerializer

    def get_serializer_context(self):
        context = super(MealsViewSet, self).get_serializer_context()
        context.update({"user_id": self.request.user.id})
        return context


class ChefMealsByCategoryView(MealsByCategoryView):
    def get_queryset(self):
        category_id = self.kwargs['cat_id']
        chef_id = self.kwargs['chef_id']
        if Category.objects.filter(id=category_id).exists() and Chef.objects.filter(id=chef_id).exists():
            queryset = Meal.objects.filter(category=category_id, chef=chef_id)
        else:
            queryset = Meal.objects.none()

        return queryset


class MealView(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ChefMealSerializer
    queryset = Meal.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request:
            context.update({"chef": self.request.user.id})

    def create(self, request, *args, **kwargs):
        res = super().create(request, *args, **kwargs)
        res.data.update({"msg": "New meal is created!"})
        return res

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        res = super().partial_update(request, *args, **kwargs)
        res.data.update({"msg": "Meal {} is updated!".format(instance.title)})
        return res

    # def get(self, request, pk=None):
    #     chef = getattr(request, "user", None)
    #     if chef is not None:
    #         if pk:
    #             meals = get_object_or_404(Meal.objects.all(), pk=pk)
    #             meal_serializer = ListMealSerializer(meals)
    #             return Response(meal_serializer.data)
    #
    #         meals = Meal.objects.filter(chef=chef)
    #         if meals:
    #             meal_serializer = ListMealSerializer(meals, many=True)
    #             return Response(meal_serializer.data, status=status.HTTP_200_OK)
    #         else:
    #             return Response({"msg": "You don't have any meals"}, status=status.HTTP_204_NO_CONTENT)
    #
    #     return Response({"msg": "User is unauthorized"}, status=status.HTTP_400_BAD_REQUEST)
    #
    # def put(self, request, pk):
    #     saved_meal = get_object_or_404(Meal.objects.all(), pk=pk)
    #     data = request.data.get('meal')
    #     serializer = ChefMealSerializer(instance=saved_meal, data=data, partial=True)
    #
    #     if serializer.is_valid():
    #         meal = serializer.save()
    #         return Response({"msg": "meal '{}' updated successfully".format(meal.title)}, status=status.HTTP_200_OK)
    #     return Response({"msg": "{}".format(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
