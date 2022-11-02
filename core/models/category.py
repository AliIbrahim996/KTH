from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=150)
    icon = models.ImageField(upload_to='???', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)