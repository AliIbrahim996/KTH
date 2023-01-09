from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from core.models import Cart, CartItem
import stripe

from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeViews(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        cart_id = request.get["cart_id"]
        try:
            cart_items = CartItem.objects.filter(cart_id=cart_id)
            line_items = []
            for cart_item in cart_items:
                meal = cart_item.meal
                line_items.append({'currency': 'usd', 'price': meal.price, 'quantity': meal.dishes_count})
            checkout_session = stripe.checkout.Session.create(
                line_items=line_items,
                mode='payment',
                metadata={'customer_id': request.user.id},
                success_url=Response({"Msg: payment sent!"}, status=status.HTTP_200_OK),  # not sure if this works
                cancel_url=Response({"Msg: payment canceled!"}, status=status.HTTP_400_BAD_REQUEST),
                # not sure of this works
            )
            return checkout_session.url
        except Exception as e:
            return str(e)
