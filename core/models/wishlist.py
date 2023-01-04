from django.db import models
from .meal import Meal
from .customer import User


class WishList(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.customer}, {self.meal}'
