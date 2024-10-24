from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.tasks import user_registration_success_mail
from utils.base_utils import get_model

User = get_model("accounts", "User")
Wallet = get_model("accounts", "Wallet")


@receiver(post_save, sender=User)
def create_wallet_instance_post_user_created(
    sender, instance, created, *args, **kwargs
):
    if created:
        Wallet.objects.create(user=instance)
        user_registration_success_mail.delay(instance.email, instance.username)
