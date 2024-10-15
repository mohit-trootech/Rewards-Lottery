from django.db import models
from django_extensions.db.models import (
    TitleSlugDescriptionModel,
    TimeStampedModel,
    ActivatorModel,
)


def _upload_to(self, filename):
    return "lotteries/{slug}/{filename}".format(slug=self.slug, filename=filename)


class Lottery(TitleSlugDescriptionModel, TimeStampedModel, ActivatorModel):
    image = models.ImageField(upload_to=_upload_to)
    vendor = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="created_lotteries"
    )
    buyer = models.ManyToManyField("accounts.User", related_name="lotteries")
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Lottery"
        verbose_name_plural = "Lotteries"

    def __str__(self):
        return self.slug


class Winner(TimeStampedModel):
    lottery = models.ForeignKey(
        "rewards.Lottery", on_delete=models.CASCADE, related_name="winners"
    )
    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="won_lotteries"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Winner"
        verbose_name_plural = "Winners"

    def __str__(self):
        return f"{self.user} won {self.amount} in {self.lottery}"
