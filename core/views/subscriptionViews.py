from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from core.models import Subscription, Chef
from django.db.models import Q
from core.serializer import ChefListSerializer, SubscriptionSerializer


class CustomerSubscriptionView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ChefListSerializer

    def get(self, request):
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


class CustomerSubscribeChefView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SubscriptionSerializer

    def post(self, request):
        subscription_serializer = SubscriptionSerializer(data=request.data)
        if subscription_serializer.is_valid():
            subscription_serializer.save()
            return Response(
                {"msg": "Chef is subscribed!"}, status=status.HTTP_201_CREATED
            )
        return Response(subscription_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
