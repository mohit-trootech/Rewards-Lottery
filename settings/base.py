from pathlib import Path
from os import path
from dotenv import dotenv_values
from utils.constants import Settings, EmailConfig
import dj_database_url
from datetime import timedelta

config = dotenv_values(".env")
AUTH_USER_MODEL = "accounts.User"
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config["SECRET_KEY"]
ROOT_URLCONF = Settings.ROOT_URL.value
APPEND_SLASH = True

# Installed Apps
# =====================================================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_extensions",
    "rest_framework_simplejwt",
    "dj_database_url",
    "debug_toolbar",
    "schema_graph",
    "accounts.apps.AccountsConfig",
    "rewards",
    "phonenumber_field",
    "rest_framework_nested",
    "celery",
    "email_validator",
    "corsheaders",
]


# Middlewares
# =====================================================
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

# Middlewares
# =====================================================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [path.join(BASE_DIR, Settings.TEMPLATE.value)],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "utils.context_processors.theme_form",
                "utils.context_processors.newsletter_form",
            ],
        },
    },
]


# WSGI Configuration
# =====================================================
WSGI_APPLICATION = "rewards.wsgi.application"

# Database
# =====================================================
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
DATABASES = {}
DATABASES["default"] = dj_database_url.parse(
    config.get("DJANGO_DATABASE_URL"),
)

# Password validation
# =====================================================
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# =====================================================
# https://docs.djangoproject.com/en/5.1/topics/i18n/
LANGUAGE_CODE = Settings.LANGUAGE_CODE.value
TIME_ZONE = Settings.TIME_ZONE.value
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# =====================================================
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_URL = Settings.STATIC_URL.value
STATICFILES_DIRS = [path.join(BASE_DIR, Settings.STATICFILES_DIRS.value)]
STATIC_ROOT = Settings.STATIC_ROOT.value

# Media files (CSS, JavaScript, Images)
# =====================================================
MEDIA_URL = Settings.MEDIA_URL.value
MEDIA_ROOT = path.join(BASE_DIR, Settings.MEDIA_ROOT.value)


# Default primary key field type
# =====================================================
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = Settings.DEFAULT_AUTO_FIELD.value


# Email Configuration
# =====================================================
EMAIL_BACKEND = EmailConfig.EMAIL_BACKEND.value
EMAIL_HOST = EmailConfig.EMAIL_HOST.value
EMAIL_USE_SSL = True  # use port 465
EMAIL_USE_TLS = False  # use port 587
EMAIL_PORT = EmailConfig.PORT_465.value if EMAIL_USE_SSL else EmailConfig.PORT_587.value
EMAIL_HOST_USER = config.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config.get("EMAIL_HOST_PASSWORD")

# Django Debug Toolbar Configuration
# =====================================================
INTERNAL_IPS = [Settings.DEBUG_TOOLBAR_IP.value]
DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.history.HistoryPanel",
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.alerts.AlertsPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
    "debug_toolbar.panels.profiling.ProfilingPanel",
]

# Rest Framework Configuration
# https://www.django-rest-framework.org/
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
        "utils.permissions.IsOwner",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

# Celery Configuration
# CELERY_BROKER_URL = "db+postgresql://mohit-trootech:postgres@localhost:5432/rewards"
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_TIMEZONE = "Asia/Kolkata"
# CELERY_BROKER_URL = "redis://default:a98t14FfJCfAC05tTjB2bwvpsJSfq43n@redis-10158.c301.ap-south-1-1.ec2.redns.redis-cloud.com:10158"
CELERY_RESULT_BACKEND = "redis"
CELERY_RESULT_EXTENDED = True
CELERY_BEAT_SCHEDULE = {
    "draw_winners": {
        "task": "rewards.tasks.draw_winners",
        "schedule": 300.0,
    },
}


# Logging Configuration

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",  # Use curly braces for string formatting
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "debug.log",
            "formatter": "verbose",
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "rewards": {
            "handlers": ["file", "console"],
            "level": "INFO",
            "propagate": True,
        },
    },
}
