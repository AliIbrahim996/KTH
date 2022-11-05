from django.db import models

class ChefAddress(models.Model):
    street = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100,)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.street