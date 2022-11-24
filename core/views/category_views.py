from rest_framework import viewsets
from core.models import Category
from core.serializer import CategorySerializer

class CategoryView(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer