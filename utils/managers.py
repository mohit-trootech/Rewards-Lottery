# Custom Managers for Models
from django.db import models


class LotteryManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("vendor")
            .prefetch_related("buyers", "buyers__user")
        )


class LotteryCashManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("lottery")


class BuyerWinnerBaseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("user")
