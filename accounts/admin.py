from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import Account


@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = (
        "email",
        "role",
        "is_active",
        "is_staff",
    )
    list_filter = (
        "role",
        "is_active",
        "is_staff",
    )
    search_fields = (
        "email",
        "first_name",
        "last_name",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Account details",
            {
                "fields": (
                    "role",
                    "is_email_verified",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Account details",
            {
                "fields": (
                    "email",
                    "role",
                    "is_email_verified",
                )
            },
        ),
    )
