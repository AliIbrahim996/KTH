from django.db import models

from core.models.customer import Customer
from core.models.meal import Meal

class Cart(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=False, null=False)
    items = models.ManyToManyField(Meal)  