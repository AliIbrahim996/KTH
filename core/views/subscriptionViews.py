from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework import permissions
from core.models import Subscription, Chef
from django.db.models import Q
from core.serializer import SubscriptionSerializer, ChefListSerializer

class CustomerSubscribeChefView(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SubscriptionSerializer
    lookup_field = ['chef_id', 'pk']

    def get_queryset(self):
        return self.request.user.subscription_set

    def get_serializer_context(self):
        context = super(CustomerSubscribeChefView, self).get_serializer_context()
        if self.request.user:
            context.update({"customer": self.request.user.id})
        if 'chef_id' in self.kwargs:
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
        subscribed_chefs_serializer = ChefListSerializer(chefs, many=True)
        un_subscribed_chefs_serializer = ChefListSerializer(un_subscribed_chefs, many=True)
        return Response({
            "subscribed_chefs": [subscribed_chefs_serializer.data],
            "un_subscribed_chefs": [un_subscribed_chefs_serializer.data]
        }, status=status.HTTP_200_OK)


    def create(self, request, *args, **kwargs):
        res = super().create(request, *args, **kwargs)
        res.data.update({"msg": "Chef is subscribed!"})
        return res



    def destroy(self, request, *args, **kwargs):
        if 'chef_id' in self.kwargs:
            chef = Chef.objects.get(pk=self.kwargs['chef_id'])
            if Subscription.objects.filter(chef=chef, customer=self.request.user).exists():
                sub_obj = Subscription.objects.get(chef=chef, customer=self.request.user)
                sub_obj.delete()
                return Response({"msg": "Chef is unsubscribed!"}, status=status.HTTP_200_OK)
            else:
                return Response({"msg": "No subscription found!"}, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "Missing chef id!"}, status=status.HTTP_400_BAD_REQUEST)
