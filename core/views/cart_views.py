from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from rest_framework import status, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import Cart, CartItem, customer
from core.serializer import CartSerializer, CartItemSerializer


def create_cart_item(cart, meal, request):
    cart_item_serializer = CartItemSerializer(cart=cart, meal=meal, data=request.data)
    if cart_item_serializer.is_valid():
        return Response(
            {"msg": "Item added to cart!"}, status=status.HTTP_201_CREATED
        )
    else:
        return Response(cart_item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        customer_obj = getattr(request, "user", None)
        meal = getattr(request, "meal", None)
        if customer_obj is not None and meal is not None:
            cart = Cart.objects.filter(customer=customer_obj, state="open")
            if cart is None:
                cart_serializer = CartSerializer(customer_obj, data=request.data)
                if cart_serializer.is_valid():
                    cart_serializer.save()
                    cart = cart_serializer.instance
                    return create_cart_item(cart, meal, request)
                else:
                    return Response(cart_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return create_cart_item(cart, meal, request)


class CartByUserView(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    cart_item_serializer_class = CartItemSerializer

    def get_queryset(self):
        customer_obj = customer.objects.get(self.kwargs['customer_id'])
        cart = Cart.objects.filter(customer=customer_obj, state="open")
        if cart is not None:
            cart_items = CartItem.objects.filter(cart=cart)
            sub_total = cart_items.aggregate(
                total=Sum(ExpressionWrapper(
                    F('meal__price') * 'count', output_field=DecimalField())))['total']
            # check if we need to serialize meal or not.
            cart_items_data = self.cart_item_serializer_class(cart_items, many=True).data
            return Response({
                "cart_id": cart.pk,
                "cart_state": cart.state,
                "customer": cart.customer,
                "cart_items": cart_items_data,
                "sub_total": sub_total
            }, status=status.HTTP_200_OK)
        return Response({"msg": "No cart found!"}, status=status.HTTP_404_NOT_FOUND)
