from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150)
    icon = models.ImageField(upload_to="images/category/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
