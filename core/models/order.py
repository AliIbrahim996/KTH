from django.db import models
from django.utils import timezone
from core.models.customer import User
from core.models import Chef


class Order(models.Model):
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered_date = models.DateTimeField(default=timezone.now)
    review = models.TextField(null=True, blank=True)
    location = models.ForeignKey("Location", null=True, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.id}'