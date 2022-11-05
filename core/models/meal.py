from django.db import models
from .chef import Chef

class Category(models.Model):
    name = models.CharField(max_length=150)
    icon = models.ImageField(upload_to='???', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class Meal(models.Model):
      
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, null=False, blank=False)
    description = models.CharField(max_length=250, null=False, blank=False)
    price = models.FloatField()
    image = models.ImageField(upload_to='images/')
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    views = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
