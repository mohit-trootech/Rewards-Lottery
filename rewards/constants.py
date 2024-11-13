"""Rewards App Constants"""

from django.utils.translation import gettext_noop as _


class ModelVerbose:
    """Rewards Model Verbose"""

    # Email Template Model
    EMAIL_TEMPLATE = "Email Template"
    EMAIL_TEMPLATES = "Email Templates"
    SUBJECT = "Subject"
    BODY = "Body"
    IS_HTML = "HTML Email Template"
    TEMPLATE = "Template"
    EMAIL_TYPES = "Email Types"

    # Lottery Model
    LOTTERY = "Lottery"
    LOTTERIES = "Lotteries"
    IMAGE = "Lottery Picture"
    LOTTERY_FK_USER = "lotteries"
    PRICE = "Price"
    EXPIRY_DATE = "Expiry Date"
    WINNING = "Winning"
    TOTAL_DRAW = "Total Draw"
    SLUG = "Slug"
    VENDOR = "Vendor"

    # Lottery Cash Model
    LOTTERY_CASH = "Lottery Cash"
    LOTTERIES_CASH = "Lotteries Cash"
    AMOUNT = "Amount"
    LOTTERY_CASH_O2O_LOTTERY = "lottery_cash"
    LOTTERY_CASH_STR = "{amount} in {lottery}"

    # Buyer Model
    BUYER = "Buyer"
    BUYERS = "Buyers"
    BUYER_FK_LOTTERY = "buyers"
    BUYER_FK_USER = "lotteries_purchased"
    QUANTITY = "Quantity"
    BUYER_STR = "{user} Purchased Lottery {lottery}"

    # Winner Model
    WINNER = "Winner"
    WINNERS = "Winners"
    WINNER_FK_LOTTERY = "winners"
    WINNER_FK_USER = "lotteries_won"
    WINNER_STR = "{user} Won Lottery {lottery}"

    # Order Model
    ORDER = "Order"
    ORDERS = "Orders"
    PAYEE = "Payee"
    EMAIL = "Email"
    AMOUNT = "Amount"
    STATUS = "Status"
    ORDER_O2O_TRANSACTION = "order"
    ORDER_FK_USER = "orders"
    ORDER_STR = "{payer} paid {amount} status {status}"


class Choice:
    """Email Template Choices"""

    REGISTERATION = "registration"
    VERIFICATION = "verification"
    RESET_PASSWORD = "reset_password"
    CHANGE_PASSWORD = "change_password"
    LOTTERY_DRAWN = "lottery_drawn"
    WINNING = "winning"
    TRANSACTION = "transaction"
    WALLET_TOPUP = "wallet_topup"
    EMAIL_TYPES = (
        (REGISTERATION, _("Registration Mail")),
        (VERIFICATION, _("Verification Mail")),
        (RESET_PASSWORD, _("Reset Password Mail")),
        (CHANGE_PASSWORD, _("Change Password Mail")),
        (LOTTERY_DRAWN, _("Lottery Drawn Mail")),
        (WINNING, _("Winning Mail")),
        (TRANSACTION, _("Transaction Mail")),
        (WALLET_TOPUP, _("Wallet Topup Mail")),
    )


class ValidationErrors:
    """Rewards API Validation Errors"""

    USER_DOES_NOT_EXISTS = _("User Does Not Exists")
    NOT_ENOUGH_AMOUNT = _("Not Enough Amount to Purchase Lottery")


class SerializerConstants:
    """Rewards API Serializer Constants"""

    # Lottery Serializer
    LOTTERIES_DETAIL = "lotteries-detail"

    LOTTERIES_LIST = "lotteries-list"
    BUYERS_DETAIL = "buyers-detail"
    WINNERS_DETAIL = "winners-detail"
    PK = "pk"
    NOT_VENDOR = "Only Vendor is Authorized to Create Lotteries"


class LookUps:
    """Rewards API Look Ups"""

    USER_USERNAME = "user__username"
    USERNAME = "username"
    SLUG = "slug"
    PK = "pk"


class TransactionDescriptions:
    LOTTERY_PURCHASE = "Lottery Purchased"
    WALLET_TOPUP = "Wallet Topup"
    LOTTERY_WON = "Lottery Won"
    LOTTERY_COMMISSION = "Lottery Drawn Commission"
