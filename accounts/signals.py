from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User, Wallet


@receiver(post_save, sender=User)
def create_wallet_instance_post_user_created(
    sender, instance, created, *args, **kwargs
):
    if created:
        Wallet.objects.create(user=instance)
