from django.contrib import admin
from .core_user_admin import CoreUserAdmin

from core.models import (
    Address,
    Chef,
    User,
    Meal,
    Order,
    Documents,
    Subscription,
    Offer,
    Complaint,
    Category,
)

admin.site.register(Address)
admin.site.register(Chef)
admin.site.register(User, CoreUserAdmin)
admin.site.register(Meal)
admin.site.register(Order)
admin.site.register(Documents)
admin.site.register(Subscription)
admin.site.register(Offer)
admin.site.register(Complaint)
admin.site.register(Category)
