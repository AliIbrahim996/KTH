from django.db import models
from .chef import Chef
from .customer import User


class Subscription(models.Model):
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.customer}, {self.chef}'
