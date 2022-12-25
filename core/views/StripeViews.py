from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
# import order from core.models import
import stripe

from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeViews(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        order_id = request.get["order_id"]
        try:
            # order = Order.objects.get(pk=order_id)
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'currency': 'usd',
                        'price': '{{PRICE_ID}}',
                        'quantity': 1,  # Get the quantity from the order,
                        'order_data': {''}  # Get all the data. maybe use order serializer.
                    },
                ],
                mode='payment',
                metadata={'product_id': 'add the order id'},
                success_url=Response({"Msg: payment sent!"}, status=status.HTTP_200_OK),  # not sure if this works
                cancel_url=Response({"Msg: payment canceled!"}, status=status.HTTP_400_BAD_REQUEST),
                # not sure of this works
            )
            return checkout_session.url
        except Exception as e:
            return str(e)
