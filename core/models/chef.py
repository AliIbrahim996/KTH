from django.db import models
from .customer import User


class Chef(models.Model):
    class ChefStates(models.TextChoices):
        PENDING = "pending"
        REJECTED = "rejected"
        APPROVED = "approved"
    
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    #location on map
    loc_lat = models.DecimalField(max_digits=9, decimal_places=6)
    loc_lan = models.DecimalField(max_digits=9, decimal_places=6)
    state = models.CharField(
        max_length=25,
        choices=ChefStates.choices,
        null=False,
        blank=False,
        default=ChefStates.PENDING
        )
    id_card = models.ImageField(upload_to='images/')
    heart_number = models.IntegerField(default = 0)
      
    def __str__(self):
        return self.full_name


class Documents(models.Model):
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='images/')