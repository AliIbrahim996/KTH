from rest_framework import viewsets
from rest_framework import permissions
from core.serializer import OrderSerializer
from core.models import Order


class OrderDetailsView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = OrderSerializer

    def get_queryset(self):
        if 'pk' in self.kwargs:
            return Order.objects.filter(pk=self.kwargs['pk'])
