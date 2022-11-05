from django.contrib import admin
from core.models import ChefAddress, Chef, Customer, Meal, Order, Documents

admin.site.register(ChefAddress)
admin.site.register(Chef)
admin.site.register(Customer)
admin.site.register(Meal)
admin.site.register(Order)
admin.site.register(Documents)