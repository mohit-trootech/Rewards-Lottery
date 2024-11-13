"""Accounts App Constants"""

from django.utils.translation import gettext_noop as _


class AuthMessages:
    """Auth Messages Constants"""


class ValidationErrors:
    """Validation Error Messages"""

    INVALID_AGE = _("Age must be 18+")
    UNMATCHED_PASSWORDS = _("Passwords do not match")


class ModelVerbose:
    """Model Verbose Names"""

    # User Model
    USER = _("User")
    USERS = _("Users")
    PROFILE_IMAGE = _("Profile Image")
    PROFILE_OPTIONS = _("Profile Options")
    AGE = _("Age")
    EMAIL = _("Email")
    PHONE = _("Contact Number")
    REGION_IN = "IN"
    GENDER = _("Gender")
    ADDRESS = _("Address")
    GOOGLE_ID = _("Google ID")

    # Wallet Model
    WALLET = _("Wallet")
    WALLETS = _("Wallets")
    WALLET_O2O_USER = _("wallet")
    BALANCE = _("Balance")
    WALLET_STR = _("{username}'s Wallet")

    # Transaction Model
    TRANSACTION = _("Transaction")
    TRANSACTIONS = _("Transactions")
    TRANSACTION_FK_USER = _("transactions")
    AMOUNT = _("Amount")
    OPTION = _("Option")
    DESCRIPTION = _("Description")
    TRANSACTION_STR = _("{username}'s {option} Transaction")


class Choices:
    """Acounts Model Choices"""

    # User Options
    VENDER = "vender"
    CUSTOMER = "customer"
    USER_TYPES = (
        (VENDER, _("Vender")),
        (CUSTOMER, _("Customer")),
    )
    # Gender Options
    MALE = "male"
    FEMALE = "female"
    GENDERS = (
        (MALE, _("Male")),
        (FEMALE, _("Female")),
    )
    # Transaction Options
    CREDIT = "credit"
    DEBIT = "debit"
    TRANSACTIONS_TYPES = (
        (CREDIT, _("Credit")),
        (DEBIT, _("Debit")),
    )


class AuthResponse:
    """Auth Api Response Messages"""

    USER_REGISTERED = _("User Registered Successfully")


class AuthExceptions:
    """Auth Api Exceptions Messages"""

    INVALID_CREDENTIALS = _("Invalid Credentials")
