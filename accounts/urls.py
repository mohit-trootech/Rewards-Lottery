from django.urls import path
from utils.constants import Urls
from accounts.api import (
    user_login,
    user_registeration,
    user_profile,
    user_password_change,
    user_email_change,
    email_verify,
    LogoutApiView,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("token/refresh/", TokenRefreshView.as_view(), name=Urls.TOKEN_REFRESH.value),
    path("login/", user_login, name=Urls.LOGIN.value),
    path("logout/", LogoutApiView.as_view(), name=Urls.LOGOUT_REVERSE.value),
    path("profile/", user_profile, name=Urls.PROFILE.value),
    path("register/", user_registeration, name=Urls.REGISTER.value),
    path("change-password/", user_password_change, name=Urls.CHANGE_PASSWORD.value),
    path("change-email/", user_email_change, name=Urls.CHANGE_EMAIL.value),
    path("verify-email/", email_verify, name=Urls.VERIFY_EMAIL.value),
]
