from django.db import models
from .order import Order
from .meal import Meal

class OrderedMeals(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='sub_orders_set')
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)