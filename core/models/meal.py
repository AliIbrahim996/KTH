from django.db import models
from .chef import Chef


class Meal(models.Model):
      
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=250,blank=True)
    price = models.FloatField()
    image = models.ImageField(upload_to='images/')
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    views = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    #food or dessert ??
    #category=models.CharField(max_length=200,null=True,choices=category)

    def __str__(self):
        return self.title
