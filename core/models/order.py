from django.db import models

from core.models.customer import User
from .chef import Chef


class Order(models.Model):

    class OrderStates(models.TextChoices):
        PENDING = "pending"
        SCHEDULED = "scheduled"
        Paid = "paid"
        DELIVERED = "delivered"


    chef = models.ForeignKey(Chef, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered_date = models.DateTimeField(auto_now_add=True)
    total_price = models.FloatField(default=0)
    review = models.TextField(null=True, blank=True)
    state = models.CharField(
        max_length=25,
        choices=OrderStates.choices,
        null=False,
        blank=False,
        default=OrderStates.PENDING
        )

    def __str__(self):
        return self.id


