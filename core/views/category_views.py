from rest_framework import viewsets, permissions
from django.db.models import Prefetch
from core.models import Category, Chef, Meal
from core.serializer import CategorySerializer, ChefCategorySerializer
from rest_framework.generics import get_object_or_404
import datetime


class CategoryView(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ChefCategoryView(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ChefCategorySerializer

    def get_queryset(self):
        chef_id = self.kwargs['chef_id']
        date = self.kwargs['date']
        chef = get_object_or_404(Chef, pk=chef_id)
        categories_id = Meal.objects.filter(chef=chef).values("category")
        queryset = Category.objects.filter(id__in=categories_id)
        return queryset.prefetch_related(
            Prefetch('meal_set', queryset=Meal.objects.filter(chef=chef, delivery_time__gte=datetime.datetime.strptime(date, "%Y-%m-%d").date())))
