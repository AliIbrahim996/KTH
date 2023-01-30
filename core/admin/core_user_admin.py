from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from core.models import User


class CoreUserAdmin(UserAdmin):
    model = User

    fieldsets =  (
        (None, {'fields': ('phone_number', 'password',)}),
        (_("Personal info"), {"fields": ("full_name", "profile_img")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    ordering = ("phone_number",)
    list_display = ("phone_number", "full_name", "is_staff")
    search_fields = ("phone_number", "full_name")
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone_number", "password1", "password2"),
            },
        ),
    )