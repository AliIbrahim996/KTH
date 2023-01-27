from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.http import Http404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import Cart, CartItem, Meal
from core.serializer import CartSerializer, CartItemSerializer, CartMealSerializer


def create_cart_item(cart, meal, request):
    cart_item_serializer = CartItemSerializer(cart=cart, meal=meal, data=request.data)
    if cart_item_serializer.is_valid():
        is_scheduled = request.data["is_scheduled"]
        cart_item = cart_item_serializer.instance
        cart_item.is_scheduled = is_scheduled
        if is_scheduled:
            is_scheduled.order_date = request.data["order_date"]
        cart_item.save()
        cart_item_serializer.save()
        return Response(
            {"msg": "Item added to cart!"}, status=status.HTTP_201_CREATED
        )
    else:
        return Response(cart_item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def update_cart_item(cart_item, cart, meal_obj, request):
    cart_item_serializer = CartItemSerializer(instance=cart_item, data=request.data, partial=True,
                                              meal=meal_obj, cart=cart)
    if cart_item_serializer.is_valid():
        cart_item_serializer.save()
        return Response({"msg": "Item count updated!"},
                        status=status.HTTP_200_OK)
    return Response({"msg": "{}".format(cart_item_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)


class CartView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk):
        try:
            return CartItem.objects.get(pk=pk)
        except CartItem.DoesNotExist:
            raise Http404

    def post(self, request):
        user = request.user
        meal = request.data["meal"]
        if user is not None and meal is not None:
            if Meal.objects.get(pk=meal).dishes_count >= request.data["count"]:
                cart = Cart.objects.filter(customer=user, state="opened")
                meal_obj = Meal.objects.get(pk=meal)
                if not cart:
                    cart_serializer = CartSerializer(customer=user, data=request.data)
                    if cart_serializer.is_valid():
                        cart_serializer.save()
                        cart = cart_serializer.instance
                        return create_cart_item(cart, meal_obj, request)
                    else:
                        return Response(cart_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                cart_item_set = cart.prefetch_related("cart_item_set").get().cart_item_set
                if cart_item_set.first():
                    chef_id = cart_item_set.first().meal.chef.id
                    if meal_obj.chef.id == chef_id:
                        cart_item = cart_item_set.filter(meal=meal_obj)
                        if not cart_item:
                            return create_cart_item(cart[0], meal_obj, request)
                        return update_cart_item(cart_item[0], cart[0], meal_obj, request)
                    return Response({"Meals must be related to chef {}".format(meal_obj.chef.user.full_name)},
                                    status=status.HTTP_400_BAD_REQUEST)
                return create_cart_item(cart[0], meal_obj, request)
            return Response({"The requested number of dishes is unavailable!"},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({"Invalid user or meal {}"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user = request.user
        meal = request.data["meal"]
        if user is not None and meal is not None:
            if Meal.objects.get(pk=meal).dishes_count >= request.data["count"]:
                cart = Cart.objects.filter(customer=user, state="opened")
                meal_obj = Meal.objects.get(pk=meal)
                cart_item = cart.prefetch_related("cart_item_set").get().cart_item_set.filter(meal=meal_obj)[0]
                return update_cart_item(cart_item, cart[0], meal_obj, request)
            return Response({"The requested number of dishes is unavailable!"},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({"Invalid user or meal {}"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = request.user
        cart = Cart.objects.filter(customer=user, state="opened")
        if cart:
            cart_items = CartItem.objects.filter(cart=cart[0])
            sub_total = cart_items.aggregate(
                total=Sum(ExpressionWrapper(F('meal__price') * F('count'), output_field=DecimalField())))['total']
            cart_items_data = CartMealSerializer(cart[0]).data
            if cart_items.first():
                delivery_cost = cart_items.first().meal.chef.delivery_cost
            else:
                delivery_cost = 0
            return Response({
                "cart_items": cart_items_data,
                "sub_total": sub_total if sub_total else 0,
                "delivery_cost": delivery_cost,
                "total":  sub_total + delivery_cost if sub_total else delivery_cost
            }, status=status.HTTP_200_OK)
        return Response({"msg": "No cart found!"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        cart_item = self.get_object(request.data["cart_item_id"])
        cart_item.delete()
        return Response({"msg: Item removed from cart!"}, status=status.HTTP_200_OK)
