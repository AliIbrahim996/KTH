from rest_framework import viewsets
from rest_framework import permissions
from core.models import Meal, Category, Chef
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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request:
            context.update({"chef_id": self.request.user.id})
        return context

    def get_queryset(self):

        if 'pk' in self.kwargs:
            return Meal.objects.filter(pk=self.kwargs['pk'])
        return Meal.objects.none()

    def create(self, request, *args, **kwargs):
        res = super().create(request, *args, **kwargs)
        res.data.update({"msg": "New meal is created!"})
        return res

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        res = super().partial_update(request, *args, **kwargs)
        res.data.update({"msg": "Meal {} is updated!".format(instance.title)})
        return res
