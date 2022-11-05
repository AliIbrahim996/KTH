from django.db import models
from .chef import Chef
from .category import Category

class Meal(models.Model):
      
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, null=False, blank=False)
    description = models.CharField(max_length=250, null=False, blank=False)
    price = models.FloatField()
    image = models.ImageField(upload_to='images/')
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    dishes_count = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    category = models.ForeignKey(Category)

    def __str__(self):
        return self.title
