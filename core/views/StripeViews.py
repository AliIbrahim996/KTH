from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from core.models import Cart, CartItem
import stripe

from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeViews(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        cart_id = request.data["cart_id"]
        try:
            cart_items = CartItem.objects.filter(cart_id=cart_id)
            line_items = []
            for cart_item in cart_items:
                meal = cart_item.meal
                line_items.append(
                    {'price_data': {'currency': 'eur', 'product_data': {'name': meal.title, 'price': meal.price, }},
                     'quantity': meal.dishes_count})

            checkout_session = stripe.checkout.Session.create(
                line_items=line_items,
                mode='payment',
                metadata={'customer_id': request.user.id},
                success_url="success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url="cancelled/",
            )
            return Response("URL: " + checkout_session.url, status=status.HTTP_200_OK)
        except Exception as e:
            return Response("Error: " + str(e), status=status.HTTP_400_BAD_REQUEST)


def webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return Response({"msg: Invalid payload"}, status=status.HTTP_400_BAD_REQUEST)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return Response({"msg: Invalid signature"}, status=status.HTTP_400_BAD_REQUEST)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # create order

        # Set cart to closed

        return Response("New order is created!", status=status.HTTP_201_CREATED)
