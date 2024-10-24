from django.contrib import admin
from utils.base_utils import get_model

User = get_model("accounts", "User")
Wallet = get_model("accounts", "Wallet")
Transaction = get_model("accounts", "Transaction")


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
    )
    readonly_fields = ("id", "last_login", "date_joined")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    fieldsets = (
        (
            None,
            {
                "fields": ["id"],
            },
        ),
        (
            "Personal Details",
            {
                "fields": ("username", "email", "password", "first_name", "last_name"),
            },
        ),
        (
            "User Details",
            {
                "fields": ("option", "age", "phone", "gender", "address"),
            },
        ),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
        ("Groups", {"fields": ("groups", "user_permissions")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("user", "balance", "created", "modified")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "option", "description", "created")
