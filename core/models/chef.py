from django.db import models
from django.contrib.auth.models import User
from .address import ChefAddress

class DocumentType(models.TextChoices):
        ID = 'personal id'
        WORK = 'work place'


class Chef(models.Model): 
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    full_name=models.CharField(max_length=50,null=False, blank=False)
    user_name=models.CharField(max_length=50,null=False, blank=False)
    phone_number = models.CharField(max_length=25, null=False, blank=False)
    email=models.EmailField(max_length=50, blank=False)
    password = models.CharField(max_length=50,null=False, blank=False)
    address = models.ForeignKey(ChefAddress, on_delete=models.CASCADE)
    #location = PlainLocationField()
    date_created=models.DateTimeField(auto_now=True)
    status=models.BooleanField()
    #id_card = models.ImageField(upload_to='images/')
    #work_place = models.ImageField(upload_to='images/')
    views = models.IntegerField(default=0)
      
    def __str__(self):
        return self.full_name
        
    def save(self,*args,**kwargs):
    	super().save(*args,**kwargs)


class Documents(models.Model):
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='images/')
    type = models.CharField(max_length=50, choices=DocumentType.choices, null=False, blank=False,
                            default=DocumentType.ID)