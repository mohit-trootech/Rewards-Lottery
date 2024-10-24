from django.db import models
from django_extensions.db.models import (
    TitleDescriptionModel,
    TimeStampedModel,
    ActivatorModel,
)
from utils.constants import Models
from utils.models import SoftDeleteActivatorModelAbstractModel
from utils.managers import LotteryManager, LotteryCashManager, BuyerWinnerBaseManager
from django_extensions.db.fields import AutoSlugField


def _upload_to(self, filename):
    return "lotteries/{slug}/{filename}".format(slug=self.slug, filename=filename)


class Lottery(
    SoftDeleteActivatorModelAbstractModel,
    TitleDescriptionModel,
    TimeStampedModel,
    ActivatorModel,
):
    image = models.ImageField(upload_to=_upload_to, null=True, blank=True)
    vendor = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name=Models.LOTTERIES_CREATED.value,
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateTimeField(blank=False, null=False)
    winning = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    total_draw = models.IntegerField(default=1)
    slug = AutoSlugField(populate_from="title", unique=True)
    objects = LotteryManager()

    class Meta:
        verbose_name = Models.LOTTERY_SINGULAR.value
        verbose_name_plural = Models.LOTTERY_PLURAL.value

    def __str__(self):
        return self.slug


class LotteryCash(SoftDeleteActivatorModelAbstractModel, ActivatorModel):
    """This model holds the lottery cash amount"""

    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    lottery = models.OneToOneField(
        "rewards.Lottery",
        on_delete=models.CASCADE,
        related_name=Models.LOTTERY_CASH.value,
    )
    objects = LotteryCashManager()

    class Meta:
        verbose_name = Models.LOTTERY_CASH_SINGULAR.value
        verbose_name_plural = Models.LOTTERY_CASH_PLURAL.value

    def __str__(self):
        return f"{self.amount} in {self.lottery}"


class Buyer(SoftDeleteActivatorModelAbstractModel, TimeStampedModel):
    lottery = models.ForeignKey(
        "rewards.Lottery", on_delete=models.CASCADE, related_name=Models.BUYERS.value
    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name=Models.LOTTERIES_BOUGHT.value,
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    objects = BuyerWinnerBaseManager()

    class Meta:
        verbose_name = Models.BUYER_SINGULAR.value
        verbose_name_plural = Models.BUYER_PLURAL.value

    def __str__(self):
        return f"{self.user} bought {self.amount} in {self.lottery}"


class Winner(SoftDeleteActivatorModelAbstractModel, TimeStampedModel):
    lottery = models.ForeignKey(
        "rewards.Lottery", on_delete=models.CASCADE, related_name=Models.WINNERS.value
    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name=Models.LOTTERIES_WON.value,
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    objects = BuyerWinnerBaseManager()

    class Meta:
        verbose_name = Models.WINNER_SINGULAR.value
        verbose_name_plural = Models.WINNER_PLURAL.value

    def __str__(self):
        return f"{self.user} won {self.amount} in {self.lottery}"


class Order(TimeStampedModel):
    payer = models.CharField(max_length=132)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=132)
    transaction = models.OneToOneField(
        "accounts.Transaction",
        on_delete=models.CASCADE,
        related_name=Models.ORDER.value,
    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name=Models.ORDERS.value,
    )

    class Meta:
        verbose_name = Models.ORDER_SINGULAR.value
        verbose_name_plural = Models.ORDER_PLURAL.value

    def __str__(self):
        return f"{self.payer} paid {self.amount} status {self.status}"
