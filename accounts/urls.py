from django.urls import path
from utils.constants import Urls
from accounts.api import (
    user_login,
    user_registeration,
    LogoutApiView,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("token/refresh/", TokenRefreshView.as_view(), name=Urls.TOKEN_REFRESH.value),
    path("login/", user_login, name=Urls.LOGIN.value),
    path("logout/", LogoutApiView.as_view(), name=Urls.LOGOUT_REVERSE.value),
    path("register/", user_registeration, name=Urls.REGISTER.value),
]
