from rest_framework import viewsets, permissions
from core.models import Category
from core.serializer import CategorySerializer


class CategoryView(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
