from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from rest_framework import status, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import Cart, CartItem, User, Meal
from core.serializer import CartSerializer, CartItemSerializer, CartMealSerializer


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
        meal = request.data["meal"]
        if customer_obj is not None and meal is not None:
            cart = Cart.objects.filter(customer=customer_obj, state="open")
            meal_obj = Meal.objects.get(pk=meal)
            if cart is None:
                cart_serializer = CartSerializer(customer_obj, data=request.data)
                if cart_serializer.is_valid():
                    cart_serializer.save()
                    cart = cart_serializer.instance
                    return create_cart_item(cart, meal_obj, request)
                else:
                    return Response(cart_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # check if meal chef is same for all meals in cart
            return create_cart_item(cart, meal_obj, request)


class CartByUserView(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CartMealSerializer

    def get_queryset(self):
        customer_obj = User.objects.get(self.kwargs['customer_id'])
        cart = Cart.objects.filter(customer=customer_obj, state="open")
        if cart is not None:
            sub_total = CartItem.objects.filter(cart=cart).aggregate(
                total=Sum(ExpressionWrapper(
                    F('meal__price') * 'count', output_field=DecimalField())))['total']
            # check if we need to serialize meal or not.
            cart_items_data = self.serializer_class(Cart).data
            return Response({
                "cart_items": cart_items_data,
                "sub_total": sub_total
            }, status=status.HTTP_200_OK)
        return Response({"msg": "No cart found!"}, status=status.HTTP_404_NOT_FOUND)
