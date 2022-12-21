from rest_framework import serializers
from core.models import Cart, CartItem, Meal, customer


class CartItemSerializer(serializers.ModelSerializer):
    meal = Meal()
    cart = Cart()

    def __init__(self, meal, cart, instance=None, data=..., **kwargs):
        self.meal = meal
        self.cart = cart
        super().__init__(instance, data, **kwargs)

    class Meta:
        model = CartItem
        fields = [
            "count"
        ]

    def create(self, validated_data):
        cart_item = CartItem.objects.create(
            cart=self.cart,
            meal=self.meal,
            count=validated_data["count"],
        )
        return cart_item


class CartSerializer(serializers.ModelSerializer):
    customer = customer

    def __init__(self, customer, instance=None, data=..., **kwargs):
        self.customer = customer
        super().__init__(instance, data, **kwargs)

    class Meta:
        model = Cart

    def create(self, validated_data):
        cart = Cart.objects.create(
            customer=self.customer,
        )
        return cart
