from django.db import models
from .customer import User


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='address_set')
    street = models.TextField(null=False, blank=False)
    city = models.CharField(max_length=100, null=False, blank=False)
    country = models.CharField(max_length=100, null=False, blank=False)
    department_numoer = models.CharField(max_length=100, null=False, blank=False)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.street