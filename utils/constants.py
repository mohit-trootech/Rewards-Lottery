from django.utils.translation import gettext_noop as _
from enum import Enum
from dotenv import dotenv_values


# Templates For Mail
class MailTemplates(Enum):
    """Mailing Templates Htmls & Txts"""

    REGISTRATION_TXT = "template/user_registration.txt"
    REGISTRATION_HTML = "template/user_registration.html"


# Celery Task Constants
class CeleryTasks(Enum):
    """Celery Taks Constants"""

    TEXT_HTML = "text/html"
    REGISTRATION_SUCCESS_MAIL = _("{username} Registered Successfully")
    REGISTRATION_MAIL_SUCCESS = _("Registration Mail Sent Successfully")
    LOTTERIES_DRAWN = _("Lotteries Drawn Successfully")
    NO_LOTTERY_AVAILABLE = _("No Lotteries Found")
    WINNING_MAIL = _("Winning Mail Sent Successfully to {username}")
    WINNER_CONGRATULATIONS = _("Congratulations {username}!")


# Model Constants
# =====================================================
class Models(Enum):
    REGION_IN = "IN"
    USER_SINGULAR = "User"
    USER_PLURAL = "Users"
    WALLET_SINGULAR = "Wallet"
    WALLET_PLURAL = "Wallets"
    TRANSACTION_SINGULAR = "Transaction"
    TRANSACTION_PLURAL = "Transactions"
    WALLET = "wallet"
    TRANSACTIONS = "transactions"
    LOTTERIES_CREATED = "created_lotteries"
    LOTTERIES_BOUGHT = "bought_lotteries"
    LOTTERIES_WON = "won_lotteries"
    LOTTERY_SINGULAR = "Lottery"
    LOTTERY_PLURAL = "Lotteries"
    BUYER_SINGULAR = "Buyer"
    BUYER_PLURAL = "Buyers"
    WINNER_SINGULAR = "Winner"
    WINNER_PLURAL = "Winners"
    BUYERS = "buyers"
    WINNERS = "winners"
    LOTTERIES = "lotteries"
    VENDOR = "vendor"
    USER = "user"
    AMOUNT = "amount"
    EXPIRY_DATE = "expiry_date"
    LOTTERY_CASH = "lottery_cash"
    LOTTERY_CASH_SINGULAR = "Lottery Cash"
    LOTTERY_CASH_PLURAL = "Lottery Cashs"
    ORDER = "order"
    ORDERS = "orders"
    ORDER_SINGULAR = "Order"
    ORDER_PLURAL = "Orders"


# User Option Constants
# =====================================================
class UserOptions(Enum):
    """User Option Constants"""

    VENDER = "Vender"
    CUSTOMER = "Customer"
    USER_TYPES = (
        (VENDER, VENDER),
        (CUSTOMER, CUSTOMER),
    )


# Gender Constants
# =====================================================
class Genders(Enum):
    """Gender Constants"""

    MALE = "Male"
    FEMALE = "Female"
    GENDERS = (
        (MALE, MALE),
        (FEMALE, FEMALE),
    )


# Transaction Option Constants
# =====================================================
class TransactionOptions(Enum):
    """Transaction Option Constants"""

    CREDIT = "credit"
    DEBIT = "debit"
    TRANSACTIONS_TYPES = (
        (CREDIT, CREDIT),
        (DEBIT, DEBIT),
    )


# Lookup Fields & Kwargs Constants
# =====================================================
class LookupFields(Enum):
    """Lookup Fields & Kwargs"""

    USER_USERNAME = "user__username"
    USERNAME = "username"
    SLUG = "slug"
    PK = "pk"


# Transaction Description Constants
# =====================================================
class TransactionDescription(Enum):
    """Transaction Desscriptions"""

    LOTTERY_PURCHASE = "Lottery Purchased"
    WALLET_TOPUP = "Wallet Topup"
    LOTTERY_WON = "Lottery Won"
    LOTTERY_COMMISSION = "Lottery Drawn Commission"


# Rewards Serilizer Constants
# =====================================================
class RewardsSerilizerConstants(Enum):
    """Rewards Serializers Constants"""

    LOTTERIES_DETAIL = "lotteries-detail"
    LOTTERIES_LIST = "lotteries-list"
    BUYERS_DETAIL = "buyers-detail"
    WINNERS_DETAIL = "winners-detail"
    PK = "pk"
    NOT_VENDOR = "Only Vendor is Authorized to Create Lotteries"


# Accounts Serilizer Constants
# =====================================================
class AccountsSerilizerConstants(Enum):
    """Accounts Serializers Constants"""

    AGE_NOT_VALID = "Must be 18+ to register & play!"


# Accounts Views Constants
# =====================================================
class AccountsViews(Enum):
    """Accounts Views Constants"""

    LOGOUT_SUCCESS = _("Logout Successfully")
    FORCE_LOGOUT_SUCCESS = _("All Sessions Cleared Successfully")
    LOGIN_SUCCESS = _("Login Successfully")
    REGISTRATION_SUCCESS = _("User Registered Successfully")
    USER_NOT_AUTHENTICATED = _("User is not authenticated")
    INVALID_CREDENTIALS = _("Invalid credentials")


# Urls Constants
# =====================================================
class Urls(Enum):
    API_ROOT = "api"
    UPDATE_API_REVERSE = "update-api"
    LOGGED_IN_USER = "logged-in-user"
    SCHEMA_REVERSE = "schema"
    TOKEN_REFRESH = "token-refresh"
    CHANGE_PASSWORD = "change-password"
    LOGIN = "login"
    LOGOUT_REVERSE = "logout"
    REGISTER = "register"
    SIGNUP = "signup"
    VERIFY_EMAIL = "verify-email"
    CHANGE_EMAIL = "change-email"
    PROFILE = "profile"
    DEMO = "demo-home"
    DETAIL_LOTTERY = "detail-lottery"
    PURCHASE_LOTTERY = "purchase-lottery"
    CREATE_LOTTERY = "create-lottery"
    TRANSACTIONS = "transactions"
    WINNING = "winning"
    FORGOT_PASSWORD = "forgot-password"
    RESET_PASSWORD = "reset-password"


# API Key Constants
# =====================================================
class ApiKey(Enum):
    API_KEY = "api_key"
    API_KEY_GENERATE = "generate_api_key"
    API_KEY_UPDATE = "update_api_key"
    API_KEY_DELETE = "delete_api_key"


# Error Messages
# =====================================================
class Errors(Enum):
    INVALID_JSON = _("Invalid JSON data")
    LOGIN_ERROR = _("Failed to Login Try Again with Correct Credentials")
    PASSWORD_NOT_MATCH = _("Please Check Passwords are Not Matching")
    UNIQUE_USER_ERROR = _("User with Same Username or Password Already Exists")
    TERMS_NOT_ACCEPTED = _("Please Accept Terms and Conditions")
    API_KEY_NOT_FOUND = _("API Key Not Found")
    API_KEY_ALREADY_EXISTS = _("API Key Already Exists")
    API_KEY_INVALID = _("Invalid API Key")
    API_KEY_UNAUTHORIZED = _(
        "Unauthorized API Key, Please Check API Key or Try Generate a New One."
    )


# Success Messages
# =====================================================
class Success(Enum):
    REGISTERED = _("User Added Successfully")
    USER_404 = _("User Does Not Exists")
    USER_UPDATED = _("User updated successfully")
    LOGGED_IN = _("Logged in Successfully")
    SIGNED_UP = _("User Registered Successfully")
    LOGGED_OUT = _("User Logged Out Successfully")
    PROFILE_UPDATED = _("Profile Updated Successfully")
    NEWSLETTER_SUCCESS = _("Newsletter Subscribed Successfully")
    API_KEY_UPDATED = _("API Key Updated Successfully")


# JsonResponses Constants
# =====================================================
class JsonResponses(Enum):
    INVALID_API = "Invalid Api Key"
    API_KEY_UNAUTHORIZED = (
        "Unauthorized API Key, Please Check API Key or Try Generate a New One."
    )


# Settings Constants
# =====================================================
class Settings(Enum):
    ROOT_URL = "rewards.urls"
    TEMPLATE = "templates/"
    STATIC_URL = "static/"
    STATICFILES_DIRS = "templates/static/"
    STATIC_ROOT = "assets/"
    MEDIA_URL = "media/"
    MEDIA_ROOT = "media/"
    LANGUAGE_CODE = "en-us"
    TIME_ZONE = "Asia/Kolkata"
    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
    DEBUG_TOOLBAR_IP = "127.0.0.1"
    CACHE_TABLE_NAME = "cache_table"
    FIRESTORE_CERTIFICATE_PATH = ".json/certificate.json"
    STORAGE_BUCKET = "STORAGE_BUCKET"


# Status
# =====================================================
class Status(Enum):
    STATUS_INACTIVE = False
    STATUS_ACTIVE = True
    STATUS_200 = 200
    STATUS_202 = 202
    STATUS_204 = 204
    STATUS_400 = 400
    STATUS_404 = 404
    STATUS_500 = 500


# Admin Action Description
# =====================================================
class AdminAction(Enum):
    USER_ADMIN_STATUS_UNACTIVE_DESCRIPTION = _("Mark Selected Items Unactive")
    USER_ADMIN_STATUS_ACTIVE_DESCRIPTION = _("Mark Selected Items Active")
    USER_INACTIVE_SUCCESS_MESSAGE = _("%d users were successfully been inactive.")
    USER_ACTIVE_SUCCESS_MESSAGE = _("%d users were successfully been active.")


# Templates Name
# =====================================================
class Templates(Enum):
    INDEX = "rewards/index.html"
    ABOUT = "rewards/about.html"
    PROFILE = "accounts/profile.html"
    LOGIN = "accounts/login.html"
    SIGNUP = "accounts/signup.html"


# App Names
# =====================================================
class AppNames(Enum):
    REWARDS = "rewards"


# Routers Basename
# =====================================================
class BaseNames(Enum):
    USERS = "users"
    WALLET = "wallet"
    TRANSACTION = "transaction"
    LOTTERIES = "lotteries"
    BUYERS = "buyers"
    WINNERS = "winners"
    ORDERS = "orders"


# Email Configurations
# =====================================================
class EmailConfig(Enum):
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.gmail.com"
    PORT_465 = 465
    PORT_587 = 587


# Request KEY
# =====================================================
class RequestKey(Enum):
    pass


# Response KEY
# =====================================================
class ResponseKey(Enum):
    pass


# Email Secret
# =====================================================
class EmailConstants(Enum):
    config = dotenv_values(".env")
    NEWSLETTER = _("QuickReads Newsletter Subscribed")
    HOST = config.get("EMAIL_HOST_USER")


# Other Constants
# =====================================================
EMPTY_STR = ""
UTF_8 = "utf-8"
FORM_CLASS = "input input-bordered w-full"
FORM_CLASS_FILE = "file-input file-input-bordered w-full"
TEXT_AREA = "textarea textarea-bordered textarea-lg w-full"
SELECT_CLASS = "select select-bordered w-full select-sm"
THEME_CHOICES = (
    ("light", "light"),
    ("dark", "dark"),
    ("cupcake", "cupcake"),
    ("bumblebee", "bumblebee"),
    ("emerald", "emerald"),
    ("corporate", "corporate"),
    ("synthwave", "synthwave"),
    ("retro", "retro"),
    ("cyberpunk", "cyberpunk"),
    ("valentine", "valentine"),
    ("halloween", "halloween"),
    ("garden", "garden"),
    ("forest", "forest"),
    ("aqua", "aqua"),
    ("lofi", "lofi"),
    ("pastel", "pastel"),
    ("fantasy", "fantasy"),
    ("wireframe", "wireframe"),
    ("black", "black"),
    ("luxury", "luxury"),
    ("dracula", "dracula"),
    ("cmyk", "cmyk"),
    ("autumn", "autumn"),
    ("business", "business"),
    ("acid", "acid"),
    ("lemonade", "lemonade"),
    ("night", "night"),
    ("coffee", "coffee"),
    ("winter", "winter"),
    ("dim", "dim"),
    ("nord", "nord"),
    ("sunset", "sunset"),
)

TYPE_HTML = "text/html"
