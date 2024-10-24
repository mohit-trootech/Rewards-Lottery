from celery import shared_task
from random import choice
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.db import transaction
from utils.utils import get_lotteries
from utils.base_utils import get_model
from utils.constants import Choices, TransactionDescription, CeleryTasks

Transaction = get_model("accounts", "Transaction")
Winner = get_model("rewards", "Winner")
LotteryCash = get_model("rewards", "LotteryCash")


@shared_task
def user_lottery_winning_mail(email, username):
    """Send email notification to a user upon winning a lottery."""
    sender = settings.EMAIL_HOST_USER
    receiver = email
    subject = CeleryTasks.WINNER_CONGRATULATIONS.value.format(username=username)
    text_template = render_to_string(
        "template/winner.txt", context={"username": username}
    )
    html_template = render_to_string(
        "template/winner.html", context={"username": username}
    )
    msg = EmailMultiAlternatives(
        subject=subject, from_email=sender, to=[receiver], body=text_template
    )
    msg.attach_alternative(html_template, "text/html")
    msg.send()
    return CeleryTasks.WINNING_MAIL.value


@shared_task
@transaction.atomic  # Ensure atomicity for data integrity
def draw_winners():
    """Draw winners for expired lotteries and handle prize distribution."""
    lotteries = get_lotteries()
    if not lotteries:
        return CeleryTasks.NO_LOTTERY_AVAILABLE.value

    for lottery in lotteries:
        lottery_cash = LotteryCash.objects.get(lottery=lottery)
        eligible_buyers = lottery.buyers.exclude(user__email__isnull=True)
        draw_count = min(lottery.total_draw, eligible_buyers.count())
        transactions = []
        for _ in range(draw_count):
            try:
                buyer = choice(eligible_buyers)
            except IndexError:
                break

            winningamount = lottery.winning / draw_count

            Winner.objects.create(
                lottery=lottery,
                user=buyer.user,
                amount=winningamount,
            )

            buyer.user.wallet.balance += winningamount
            buyer.user.wallet.save(update_fields=["balance"])

            transactions.append(
                Transaction(
                    user=buyer.user,
                    amount=winningamount,
                    option=Choices.CREDIT.value,
                    description=TransactionDescription.LOTTERY_WON.value,
                )
            )

            lottery_cash.amount -= winningamount
            lottery_cash.save()

            user_lottery_winning_mail.delay(buyer.user.email, buyer.user.username)

            print(f"Lottery Draw {lottery.id}, Winner: {buyer.user.username}")

        _process_vendor_earnings(lottery, lottery_cash)
        Transaction.objects.bulk_create(transactions)

    return CeleryTasks.LOTTERIES_DRAWN.value


def _process_vendor_earnings(lottery, lottery_cash):
    """Helper function to process vendor earnings and close the lottery."""
    vendor_earnings = lottery_cash.amount

    Transaction.objects.create(
        user=lottery.vendor,
        amount=vendor_earnings,
        option=Choices.CREDIT.value,
        description=TransactionDescription.LOTTERY_COMMISSION.value,
    )

    lottery.vendor.wallet.balance += vendor_earnings
    lottery.vendor.wallet.save(update_fields=["balance"])

    lottery_cash.amount = 0
    lottery_cash.save()
    lottery_cash.soft_delete()
    lottery.soft_delete()
