from django.db import models
from core.models import CartItem, Order


class SubOrder(models.Model):
    class OrderStates(models.TextChoices):
        PENDING = "pending"
        PICKUP = "pickup"
        SCHEDULED = "scheduled"
        DELIVERED = "delivered"

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    state = models.CharField(
        max_length=25,
        choices=OrderStates.choices,
        null=False,
        blank=False,
        default=OrderStates.PENDING
    )
    total_price = models.FloatField(default=0)
    cart_items = models.ManyToManyField(CartItem)
