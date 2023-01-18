from django.db import models
from .chef import Chef
from .customer import User


class Subscription(models.Model):
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE, db_column="chef", related_name="subscription_set")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, db_column="customer", related_name="subscription_set")
