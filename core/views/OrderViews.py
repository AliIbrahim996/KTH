from rest_framework import viewsets
from rest_framework import permissions
from core.serializer import OrderSerializer
from core.models import Order


class OrderDetailsView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = OrderSerializer

    def get_queryset(self):
        if self.request.user:
            return Order.objects.filter(customer__id=self.request.user.id)
