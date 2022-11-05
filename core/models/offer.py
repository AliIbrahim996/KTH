from django.db import models
from .chef import Chef
from .meal import Meal

class Offer(models.Model):

    chef = models.ForeignKey(Chef, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    Discount_presentage = models.FloatField(null=False, blank=False)
    start_date = models.DateTimeField(null=False, blank=False)
    end_date = models.DateTimeField(null=False, blank=False)

    def __str__(self):
        return f'{self.Discount_presentage}, discount on {self.meal}'