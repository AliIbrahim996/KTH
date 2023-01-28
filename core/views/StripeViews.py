from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from core.models import (Cart, CartItem, Order, SubOrder, Chef)
import stripe

from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeViews(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        if request.data["cart_id"]:
            cart_id = request.data["cart_id"]
            try:
                cart_items = CartItem.objects.filter(cart_id=cart_id)
                line_items = []
                if cart_items.first():
                    delivery_cost = cart_items.first().meal.chef.delivery_cost / cart_items.count()
                else:
                    delivery_cost = 0
                for cart_item in cart_items:
                    meal = cart_item.meal
                    line_items.append(
                        {'price_data': {'currency': 'eur', 'product_data': {'name': meal.title},
                                        'unit_amount': int(meal.price * 100 + delivery_cost * 100)},
                         'quantity': cart_item.count})

                checkout_session = stripe.checkout.Session.create(
                    line_items=line_items,
                    payment_intent_data={"setup_future_usage": "off_session"},
                    payment_method_types=['card'],
                    mode='payment',
                    metadata={'customer_id': request.user.id, "cart_id": cart_id},
                    success_url="http://127.0.0.1:8000/core/customer/payment/fulfil",
                    cancel_url="http://127.0.0.1:8000/core/customer/payment/cancelled", )

                return Response("URL: " + checkout_session.url, status=status.HTTP_200_OK)
            except Exception as e:
                return Response("Error: " + str(e), status=status.HTTP_400_BAD_REQUEST)


class StripeFulfilViews(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        payload = request.body
        sig_header = request.headers['STRIPE_SIGNATURE']
        event = None
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET_KEY)
        except ValueError as e:
            # Invalid payload
            return Response({"msg: Invalid payload! " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return Response({"msg: Invalid signature! " + str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Handle the checkout.session.completed event
        if event['type'] == 'checkout.session.completed':
            # Create order
            cart_id = event['data']['object']['metadata']['cart_id']
            cart = Cart.objects.get(cart_id)
            cart_items = CartItem.objects.filter(cart_id=cart_id)
            chef_id = cart_items[0].meal.chef.id
            # Create new order
            order = Order.objects.create(chef_id=chef_id, customer=cart.customer.id)
            try:
                scheduled_items_price = non_scheduled_items_price = Chef.objects.get(pk=chef_id).delivery_cost
                scheduled_orders = SubOrder.objects.create(state=SubOrder.OrderStates.SCHEDULED, order=order)
                non_scheduled_orders = SubOrder.objects.create(state=SubOrder.OrderStates.PENDING, order=order)

                # Combine Scheduled items into one subOrder.
                for cart_item in cart_items:
                    if cart_item.is_scheduled:
                        scheduled_orders.cart_items.add(cart_item)
                        scheduled_items_price += cart_item.count * cart_item.meal.price
                # Combine non-Scheduled items into one subOrder.
                    else:
                        non_scheduled_orders.cart_items.add(cart_item)
                        non_scheduled_items_price += cart_item.count * cart_item.meal.price

                scheduled_orders.total_price = scheduled_items_price
                non_scheduled_orders.total_price = non_scheduled_items_price
                scheduled_orders.save()
                non_scheduled_orders.save()
                # Set cart to closed.
                cart.CartStates = Cart.CartStates.CLOSED
                cart.save()
                print("New order is created!")
                return Response("New order is created!", status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response("Error! " + str(e), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Unhandled event type!", status=status.HTTP_400_BAD_REQUEST)
