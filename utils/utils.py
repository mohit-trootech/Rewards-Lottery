from django.utils.timezone import now
from django.db.models import Q
from django_extensions.db.models import ActivatorModel
from rest_framework.serializers import ValidationError
from accounts.constants import Choices
from utils.base_utils import get_model

Lottery = get_model("rewards", "Lottery")


def get_lotteries():
    """get lotteries instances for upcoming draw"""
    return (
        Lottery.objects.select_related("vendor")
        .prefetch_related("buyers__user", "buyers")
        .filter(
            Q(status=ActivatorModel.ACTIVE_STATUS)
            & Q(expiry_date__lt=now())
            & Q(total_draw__gt=0)
        )
    )


def get_models_instance_else_serializer_validation_error(pk: int, model):
    """
    Function to return model instance based on pk else raise serializer ValidationError
    """

    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        raise ValidationError(f"{model.__name__}'s Object with pk {pk} Does Not Exists")


def check_whether_user_can_buy_lottery_else_validation_error(user, lotter_price):
    """
    Check whether user wallet have amount to purchase lottery else raise serializer ValidationError
    """
    if user.wallet.balance < lotter_price:
        raise ValidationError(
            f"User {user.username} Wallet Balance is Insufficient to Buy Lottery"
        )


def check_wallet_minumun_balance_criteria(user):
    """Check whether user wallet have minimum balance else raise serializer ValidationError"""
    if user.wallet.balance < 500:
        raise ValidationError("Minimum Wallet Balance is 500, Before Starting Lottery")


def check_user_options(user):
    """Check whethher user option is customer else raise serializer ValidationError Vendor Not Buy Tickets"""
    if user.option != Choices.CUSTOMER.value:
        raise ValidationError("Vendor Not Buy Tickets")
