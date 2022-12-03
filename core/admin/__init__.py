from django.contrib import admin
from core.models import (
    Address,
    Chef,
    User,
    Meal,
    Order,
    Documents,
    Subscribtion,
    Offer,
    Complaint,
    Category,
)

admin.site.register(Address)
admin.site.register(Chef)
admin.site.register(User)
admin.site.register(Meal)
admin.site.register(Order)
admin.site.register(Documents)
admin.site.register(Subscribtion)
admin.site.register(Offer)
admin.site.register(Complaint)
admin.site.register(Category)
