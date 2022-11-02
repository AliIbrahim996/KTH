from django.db import models
from .chef import Chef
from .meal import Meal
from .customer import Customer

class Complaint(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    complaint_text = models.TextField(null=False, blank=False)
    answer = models.TextField(null=True, blank=False)

    def __str__(self):
        return f'{self.customer}, {self.meal}'