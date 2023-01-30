from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from core.models import Order


class OrderRating(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    feedback = models.TextField(max_length=500, null=True, blank=False)

    def __str__(self):
        return self.id

