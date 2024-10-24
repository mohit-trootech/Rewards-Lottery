from django.contrib import admin
from rewards.models import Lottery, Winner, Buyer, LotteryCash, Order


@admin.register(LotteryCash)
class LotteryCashAdmin(admin.ModelAdmin):
    list_display = ["lottery", "amount"]
    list_filter = ["lottery"]
    search_fields = ["lottery__title"]
    raw_id_fields = ["lottery"]


@admin.register(Lottery)
class LotteryAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "slug",
        "status",
        "price",
        "expiry_date",
        "winning",
        "total_draw",
    ]
    list_filter = ["status", "expiry_date"]
    search_fields = ["title", "description", "slug"]


@admin.register(Winner)
class WinnerAdmin(admin.ModelAdmin):
    list_display = ["user", "lottery", "amount"]
    list_filter = ["lottery"]
    search_fields = ["user__username", "lottery__title"]
    raw_id_fields = ["user", "lottery"]


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ["user", "lottery", "amount"]
    list_filter = ["lottery"]
    search_fields = ["user__username", "lottery__title"]
    raw_id_fields = ["user", "lottery"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["payer", "email", "amount", "status", "user"]
    list_filter = ["status"]
    search_fields = ["payer", "email", "amount", "status", "transaction", "user"]
    raw_id_fields = ["transaction", "user"]
