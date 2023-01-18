from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from .customer import User
from .meal import Meal


class MealsRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    feedback = models.TextField(max_length=500, null=True, blank=False)

    class Meta:
        unique_together = ('user', 'meal')

    def __str__(self):
        return f'{self.user}, {self.meal}'
