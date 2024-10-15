from django.contrib.auth.models import AbstractUser
from utils.constants import Choices
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django_extensions.db.models import TimeStampedModel


def _upload_to(self, filename):
    return "users/{username}/{filename}".format(
        username=self.username, filename=filename
    )


class User(AbstractUser):
    image = models.ImageField(upload_to=_upload_to, null=True, blank=True)
    type = models.CharField(
        max_length=16,
        choices=Choices.USER_TYPES.value,
        default=Choices.CUSTOMER.value,
    )
    age = models.IntegerField(null=True, blank=True)
    phone = PhoneNumberField(region="IN", null=True, blank=True)
    gender = models.CharField(
        max_length=16, choices=Choices.GENDERS.value, null=True, blank=True
    )
    address = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username


class Wallet(TimeStampedModel):
    user = models.OneToOneField(
        "accounts.User", on_delete=models.CASCADE, related_name="wallet"
    )
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"

    def __str__(self):
        return f"{self.balance}"


class Transaction(TimeStampedModel):
    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="transactions"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=8, choices=Choices.TRANSACTIONS_TYPES.value)
    description = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def __str__(self):
        return f"{self.amount} {self.type} {self.description}"
