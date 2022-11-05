from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):

    user=models.OneToOneField(User,on_delete=models.CASCADE)
    full_name=models.CharField(max_length=50,null=False, blank=False)
    user_name=models.CharField(max_length=50,null=False, blank=False)
    phone_number = models.CharField(max_length=25, null=False, blank=False)
    email=models.EmailField(max_length=50, blank=False)
    password = models.CharField(max_length=50,null=False, blank=False)
    date_created=models.DateTimeField(auto_now=True)
      
    def __str__(self):
        return self.full_name
        
    def save(self,*args,**kwargs):
    	super().save(*args,**kwargs)