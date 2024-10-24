from django.contrib.auth.models import AbstractUser
from utils.constants import Choices
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django_extensions.db.models import TimeStampedModel
from utils.constants import Models
from utils.models import SoftDeleteActivatorModelAbstractModel


def _upload_to(self, filename):
    return "users/{username}/{filename}".format(
        username=self.username, filename=filename
    )


class User(AbstractUser):
    image = models.ImageField(upload_to=_upload_to, null=True, blank=True)
    option = models.CharField(
        max_length=16,
        choices=Choices.USER_TYPES.value,
        default=Choices.CUSTOMER.value,
    )
    age = models.IntegerField(null=True, blank=True)
    phone = PhoneNumberField(region=Models.REGION_IN.value, null=True, blank=True)
    gender = models.CharField(
        max_length=16, choices=Choices.GENDERS.value, null=True, blank=True
    )
    address = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = Models.USER_SINGULAR.value
        verbose_name_plural = Models.USER_PLURAL.value

    def __str__(self):
        return self.username


class Wallet(SoftDeleteActivatorModelAbstractModel, TimeStampedModel):
    user = models.OneToOneField(
        "accounts.User", on_delete=models.CASCADE, related_name=Models.WALLET.value
    )
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = Models.WALLET_SINGULAR.value
        verbose_name_plural = Models.WALLET_PLURAL.value

    def __str__(self):
        return f"{self.user.username}'s Wallet: {self.balance}"


class Transaction(SoftDeleteActivatorModelAbstractModel, TimeStampedModel):
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name=Models.TRANSACTIONS.value,
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    option = models.CharField(max_length=8, choices=Choices.TRANSACTIONS_TYPES.value)
    description = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = Models.TRANSACTION_SINGULAR.value
        verbose_name_plural = Models.TRANSACTION_PLURAL.value

    def __str__(self):
        return f"{self.amount} {self.option} {self.description}"
