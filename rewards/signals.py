from django.db.models.signals import post_save
from django.dispatch import receiver
from utils.base_utils import get_model

Lottery = get_model("rewards", "Lottery")
LotteryCash = get_model("rewards", "LotteryCash")
Buyer = get_model("rewards", "Buyer")


@receiver(post_save, sender=Lottery)
def create_lotter_cash(sender, instance, created, **kwargs):
    """Create LotteryCash Object When a New Lottery is Created"""
    if created:
        LotteryCash.objects.create(lottery=instance)


@receiver(post_save, sender=Buyer)
def update_lotteramount_when_lottery_purchases(sender, instance, created, **kwargs):
    """
    Update LotteryCash Object When a Buyer is Created
    """
    lottery_cash = LotteryCash.objects.get(lottery=instance.lottery)
    lottery_cash.amount += instance.amount
    lottery_cash.save()
