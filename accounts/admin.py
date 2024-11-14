from django.contrib import admin
from utils.base_utils import get_model

User = get_model("accounts", "User")
Wallet = get_model("accounts", "Wallet")
Transaction = get_model("accounts", "Transaction")
Otp = get_model("accounts", "Otp")


@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = ("user", "otp")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "option",
        "age",
        "phone",
        "gender",
        "address",
        "is_verified",
    )
    readonly_fields = ("last_login", "date_joined")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "image",
                    "option",
                    "age",
                    "phone",
                    "gender",
                    "address",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_verified",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "option",
        "gender",
        "is_verified",
    )
    search_fields = ("username", "email", "first_name", "last_name")
    readonly_fields = ("last_login", "date_joined")
    ordering = ("username",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("user", "balance", "created", "modified")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "option", "description", "created")
