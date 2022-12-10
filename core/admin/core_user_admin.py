from django.contrib.auth.admin import UserAdmin
from core.models import User


class CoreUserAdmin(UserAdmin):
    model = User

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('phone_number', 'full_name', 'profile_img',)}),
    )

    list_display = ("phone_number", "username", "email", "first_name", "last_name", "is_staff")
