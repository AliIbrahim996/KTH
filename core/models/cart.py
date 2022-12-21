from django.db import models

from core.models.customer import User


class Cart(models.Model):

    class CartStates(models.TextChoices):
        OPENED = "opend"
        CLOSED = "closed"

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.CharField(
        max_length=25,
        choices=CartStates.choices,
        null=False,
        blank=False,
        default=CartStates.OPENED
    )

    def __str__(self):
        return self.id