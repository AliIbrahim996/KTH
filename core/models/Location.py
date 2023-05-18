from django.db import models
from .customer import User


class Location(models.Model):

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="location_set")
    # location on map
    loc_lat = models.DecimalField(max_digits=9, decimal_places=6)
    loc_lan = models.DecimalField(max_digits=9, decimal_places=6)
    street = models.TextField(null=True)
    city = models.TextField(null=True)
    country = models.TextField(null=True)
    department_number = models.TextField(null=True)
    location_type = models.TextField(null=True)


    def __str__(self):
        return f'{self.id}'


class UserLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="location")
    # location on map
    street = models.TextField(null=True)
    city = models.TextField(null=True)
    state = models.TextField(null=True)
    zip_code = models.CharField(max_length=100 ,null=True)

    def __str__(self):
        return f'{self.id}'
