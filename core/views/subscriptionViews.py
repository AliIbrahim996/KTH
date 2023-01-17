from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework import permissions
from core.models import Subscription, Chef
from django.db.models import Q
from core.serializer import SubscriptionSerializer


class CustomerSubscribeChefView(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return self.request.user.subscription_set

    def get_serializer_context(self):
        context = super(CustomerSubscribeChefView, self).get_serializer_context()
        context.update({"customer": self.request.user.id})
        context.update({"chef": self.kwargs['chef_id']})
        return context

    def list(self, request, *args, **kwargs):
        customer_id = request.user.id
        # Get all subscribed chefs
        subscribed_chefs = Subscription.objects.filter(customer=customer_id).values('chef')
        chefs = Chef.objects.filter(id__in=subscribed_chefs)
        # Get all unsubscribed chefs
        un_subscribed_chefs = Chef.objects.filter(~Q(id__in=subscribed_chefs))
        # Serialize data
        subscribed_chefs_serializer = self.serializer_class(chefs, many=True)
        un_subscribed_chefs_serializer = self.serializer_class(un_subscribed_chefs, many=True)
        return Response({
            "subscribed_chefs": subscribed_chefs_serializer.data,
            "un_subscribed_chefs": un_subscribed_chefs_serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"msg": "Chef is subscribed!"}, status=status.HTTP_201_CREATED
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"msg": "Chef is unsubscribed!"}, status=status.HTTP_200_OK)
