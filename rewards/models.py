from django.db import models
from django_extensions.db.models import (
    TitleDescriptionModel,
    TimeStampedModel,
    ActivatorModel,
)
from rewards.constants import ModelVerbose, Choice
from utils.models import SoftDeleteActivatorModelAbstractModel
from utils.managers import LotteryManager, LotteryCashManager, BuyerWinnerBaseManager
from django_extensions.db.fields import AutoSlugField


def _upload_to(self, filename):
    return "lotteries/{slug}/{filename}".format(slug=self.slug, filename=filename)


class EmailTemplate(models.Model):
    """Model to store email templates"""

    subject = models.CharField(ModelVerbose.SUBJECT, max_length=255)
    body = models.TextField(ModelVerbose.BODY)
    types = models.CharField(
        choices=Choice.EMAIL_TYPES,
        verbose_name=ModelVerbose.EMAIL_TYPES,
        max_length=255,
        null=True,
        blank=True,
    )
    is_html = models.BooleanField(ModelVerbose.IS_HTML, default=False)
    template = models.TextField(ModelVerbose.TEMPLATE, null=True, blank=True)

    class Meta:
        verbose_name = ModelVerbose.EMAIL_TEMPLATE
        verbose_name_plural = ModelVerbose.EMAIL_TEMPLATES

    def __str__(self):
        return self.subject


class Lottery(
    SoftDeleteActivatorModelAbstractModel,
    TitleDescriptionModel,
    TimeStampedModel,
    ActivatorModel,
):
    """Lottery Base Model"""

    image = models.ImageField(
        verbose_name=ModelVerbose.IMAGE, upload_to=_upload_to, null=True, blank=True
    )
    vendor = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name=ModelVerbose.LOTTERY_FK_USER,
    )
    price = models.DecimalField(
        verbose_name=ModelVerbose.PRICE, max_digits=10, decimal_places=2
    )
    expiry_date = models.DateTimeField(
        verbose_name=ModelVerbose.EXPIRY_DATE, blank=False, null=False
    )
    winning = models.DecimalField(
        verbose_name=ModelVerbose.WINNING, max_digits=10, decimal_places=2, default=100
    )
    total_draw = models.IntegerField(verbose_name=ModelVerbose.TOTAL_DRAW, default=1)
    slug = AutoSlugField(
        verbose_name=ModelVerbose.SLUG, populate_from="title", unique=True
    )
    objects = LotteryManager()

    class Meta:
        verbose_name = ModelVerbose.LOTTERY
        verbose_name_plural = ModelVerbose.LOTTERIES

    def __str__(self):
        return self.slug


class LotteryCash(SoftDeleteActivatorModelAbstractModel, ActivatorModel):
    """LotteryCash Model - Holds the Lottery Cash"""

    amount = models.DecimalField(
        verbose_name=ModelVerbose.AMOUNT, max_digits=10, decimal_places=2, default=0
    )
    lottery = models.OneToOneField(
        "rewards.Lottery",
        on_delete=models.CASCADE,
        related_name=ModelVerbose.LOTTERY_CASH_O2O_LOTTERY,
    )
    objects = LotteryCashManager()

    class Meta:
        verbose_name = ModelVerbose.LOTTERY_CASH
        verbose_name_plural = ModelVerbose.LOTTERIES_CASH

    def __str__(self):
        return ModelVerbose.LOTTERY_CASH_STR.format(
            amount=self.amount, lottery=self.lottery.title
        )


class Buyer(SoftDeleteActivatorModelAbstractModel, TimeStampedModel):
    lottery = models.ForeignKey(
        "rewards.Lottery",
        on_delete=models.CASCADE,
        related_name=ModelVerbose.BUYER_FK_LOTTERY,
    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name=ModelVerbose.BUYER_FK_USER,
    )
    amount = models.DecimalField(ModelVerbose.AMOUNT, max_digits=10, decimal_places=2)
    quantity = models.IntegerField(ModelVerbose.QUANTITY, default=1)
    objects = BuyerWinnerBaseManager()

    class Meta:
        verbose_name = ModelVerbose.BUYER
        verbose_name_plural = ModelVerbose.BUYERS

    def __str__(self):
        return ModelVerbose.BUYER_STR.format(user=self.user, lottery=self.lottery.title)


class Winner(SoftDeleteActivatorModelAbstractModel, TimeStampedModel):
    lottery = models.ForeignKey(
        "rewards.Lottery",
        on_delete=models.CASCADE,
        related_name=ModelVerbose.WINNER_FK_LOTTERY,
    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name=ModelVerbose.WINNER_FK_USER,
    )
    amount = models.DecimalField(
        verbose_name=ModelVerbose.AMOUNT, max_digits=10, decimal_places=2
    )
    objects = BuyerWinnerBaseManager()

    class Meta:
        verbose_name = ModelVerbose.WINNER
        verbose_name_plural = ModelVerbose.WINNERS

    def __str__(self):
        return ModelVerbose.WINNER_STR.format(
            user=self.user, lottery=self.lottery.title
        )


class Order(TimeStampedModel):
    payer = models.CharField(ModelVerbose.PAYEE, max_length=132)
    email = models.EmailField(
        ModelVerbose.EMAIL,
    )
    amount = models.DecimalField(ModelVerbose.AMOUNT, max_digits=10, decimal_places=2)
    status = models.CharField(ModelVerbose.STATUS, max_length=132)
    transaction = models.OneToOneField(
        "accounts.Transaction",
        on_delete=models.CASCADE,
        related_name=ModelVerbose.ORDER_O2O_TRANSACTION,
    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name=ModelVerbose.ORDER_FK_USER,
    )

    class Meta:
        verbose_name = ModelVerbose.ORDER
        verbose_name_plural = ModelVerbose.ORDERS

    def __str__(self):
        return ModelVerbose.ORDER_STR.format(
            payer=self.payer, amount=self.amount, status=self.status
        )
