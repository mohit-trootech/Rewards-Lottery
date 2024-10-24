from django.urls import path
from utils.constants import Urls
from accounts.api import (
    LoginApiView,
    UserRegistrationApiView,
    LogoutApiView,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("token/refresh/", TokenRefreshView.as_view(), name=Urls.TOKEN_REFRESH.value),
    path("login/", LoginApiView.as_view(), name=Urls.LOGIN.value),
    path("logout/", LogoutApiView.as_view(), name=Urls.LOGOUT_REVERSE.value),
    path("signup/", UserRegistrationApiView.as_view(), name=Urls.SIGNUP.value),
]
