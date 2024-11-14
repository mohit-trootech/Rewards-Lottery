from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django_extensions.db.models import TimeStampedModel
from utils.models import SoftDeleteActivatorModelAbstractModel
from accounts.constants import ModelVerbose, Choices
from django.utils.timezone import now, timedelta


def _upload_to(self, filename):
    return "users/{username}/{filename}".format(
        username=self.username, filename=filename
    )


def _random_otp():
    import random

    return random.randint(100000, 999999)


class Otp(models.Model):
    otp = models.IntegerField(unique=True, default=_random_otp)
    expiry = models.DateTimeField()
    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name=ModelVerbose.OTP_O2O_USER,
    )

    class Meta:
        verbose_name = ModelVerbose.OTP
        verbose_name_plural = ModelVerbose.OTPS
        ordering = ["user__username"]

    def save(self, *args, **kwargs):
        self.expiry = now() + timedelta(minutes=5)

        return super().save(*args, **kwargs)

    def __str__(self):
        return ModelVerbose.OTP_STR.format(username=self.user.username)


class User(AbstractUser):
    email = models.EmailField(verbose_name=ModelVerbose.EMAIL, unique=True)
    image = models.ImageField(
        verbose_name=ModelVerbose.PROFILE_IMAGE,
        upload_to=_upload_to,
        null=True,
        blank=True,
    )
    option = models.CharField(
        verbose_name=ModelVerbose.PROFILE_OPTIONS,
        max_length=16,
        choices=Choices.USER_TYPES,
        default=Choices.CUSTOMER,
    )
    age = models.IntegerField(verbose_name=ModelVerbose.AGE, null=True, blank=True)
    phone = PhoneNumberField(
        verbose_name=ModelVerbose.PHONE,
        region=ModelVerbose.REGION_IN,
        null=True,
        blank=True,
    )
    gender = models.CharField(
        verbose_name=ModelVerbose.GENDER,
        max_length=16,
        choices=Choices.GENDERS,
        null=True,
        blank=True,
    )
    address = models.CharField(
        verbose_name=ModelVerbose.ADDRESS, max_length=255, null=True, blank=True
    )
    google_id = models.CharField(
        verbose_name=ModelVerbose.GOOGLE_ID, max_length=255, null=True, blank=True
    )
    is_verified = models.BooleanField(
        default=Choices.INACTIVE_STATUS,
        choices=Choices.STATUS_CHOICES,
        verbose_name=ModelVerbose.ACCOUNT_VERIFIED,
    )

    class Meta:
        verbose_name = ModelVerbose.USER
        verbose_name_plural = ModelVerbose.USERS

    def __str__(self):
        return self.username


class Wallet(SoftDeleteActivatorModelAbstractModel, TimeStampedModel):
    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name=ModelVerbose.WALLET_O2O_USER,
    )
    balance = models.DecimalField(
        verbose_name=ModelVerbose.BALANCE, max_digits=10, decimal_places=2, default=0
    )

    class Meta:
        verbose_name = ModelVerbose.WALLET
        verbose_name_plural = ModelVerbose.WALLETS

    def __str__(self):
        return ModelVerbose.WALLET_STR.format(username=self.user.username)


class Transaction(SoftDeleteActivatorModelAbstractModel, TimeStampedModel):
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name=ModelVerbose.TRANSACTION_FK_USER,
    )
    amount = models.DecimalField(
        verbose_name=ModelVerbose.AMOUNT, max_digits=10, decimal_places=2
    )
    option = models.CharField(
        verbose_name=ModelVerbose.OPTION,
        max_length=8,
        choices=Choices.TRANSACTIONS_TYPES,
    )
    description = models.CharField(
        verbose_name=ModelVerbose.DESCRIPTION, max_length=255, null=True, blank=True
    )

    class Meta:
        verbose_name = ModelVerbose.TRANSACTION
        verbose_name_plural = ModelVerbose.TRANSACTIONS

    def __str__(self):
        return ModelVerbose.TRANSACTION_STR.format(
            username=self.user.username, option=self.option
        )
