from rest_framework.viewsets import ModelViewSet
from core.serializer import OrderRateSerializer
from rest_framework.permissions import IsAuthenticated
from core.models import OrderRating


class OrderRateView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderRateSerializer

    def get_queryset(self):
        if 'pk' in self.kwargs:
            return OrderRating.objects.filter(customer__id=self.kwargs['pk'])
        else:
            return OrderRating.objects.none()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if 'pk' in self.kwargs:
            context.update({"order_id": self.kwargs['pk']})
        return context
