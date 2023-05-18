from django.db import models
from .customer import User


class Chef(models.Model):
    class ChefStates(models.TextChoices):
        PENDING = "pending"
        REJECTED = "rejected"
        APPROVED = "approved"

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # location on map
    loc_lat = models.DecimalField(max_digits=9, decimal_places=6)
    loc_lan = models.DecimalField(max_digits=9, decimal_places=6)
    state = models.CharField(
        max_length=25,
        choices=ChefStates.choices,
        null=False,
        blank=False,
        default=ChefStates.PENDING,
    )
    id_card = models.ImageField(upload_to="images/")
    cover_image = models.ImageField(upload_to="images/", null=True)
    location = models.CharField(max_length=255, null=True)
    heart_number = models.IntegerField(default=0)
    delivery_cost = models.IntegerField(default=0)
    description = models.TextField(max_length=255, null=True)
    bio = models.TextField(max_length=150, null=True)
    is_delivery = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user}'


class Documents(models.Model):
    chef = models.ForeignKey(
        Chef, on_delete=models.CASCADE, related_name="documents_set"
    )
    img = models.ImageField(upload_to="images/")
