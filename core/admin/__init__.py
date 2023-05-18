from django.contrib import admin
from .core_user_admin import CoreUserAdmin
from .order_admin import OrderAdmin, SubOrderAdmin


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
    Cart,
    CartItem,
    MealsRating,
    SubOrder,
    Location,
    WishList,
    OrderRating,
)

admin.site.register(Address)
admin.site.register(Chef)
admin.site.register(User, CoreUserAdmin)
admin.site.register(Meal)
admin.site.register(Documents)
admin.site.register(Subscription)
admin.site.register(Offer)
admin.site.register(Complaint)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(MealsRating)
+admin.site.register(Order, OrderAdmin)
+admin.site.register(SubOrder, SubOrderAdmin)
admin.site.register(Location)
admin.site.register(WishList)
admin.site.register(OrderRating)
