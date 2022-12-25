from django.db import models
from .meal import Meal
from .cart import Cart


class CartItem(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_item_set")
    count = models.IntegerField(default=1)