from django.contrib.auth.admin import UserAdmin
from accounts.models import User, Wallet, Transaction
from django.contrib import admin

admin.site.register(User, UserAdmin)

admin.site.register(Wallet)
admin.site.register(Transaction)
