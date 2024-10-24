from django.urls import path
from demo.views import (
    demo_home,
    create_lottery,
    detail_lottery,
    purchase_lottery,
    transactions_view,
    winning_view,
    login_view,
    signup_view,
    profile_view,
)
from utils.constants import Urls

app_name = "demo"
urlpatterns = [
    path("", demo_home, name=Urls.DEMO.value),
    path("lottery/<slug>/", detail_lottery, name=Urls.DETAIL_LOTTERY.value),
    path("purchase/<slug>/", purchase_lottery, name=Urls.PURCHASE_LOTTERY.value),
    path("create/", create_lottery, name=Urls.CREATE_LOTTERY.value),
    path("transactions/", transactions_view, name=Urls.TRANSACTIONS.value),
    path("winning/", winning_view, name=Urls.WINNING.value),
    path("login/", login_view, name=Urls.LOGIN.value),
    path("signup/", signup_view, name=Urls.SIGNUP.value),
    path("profile/<slug>/", profile_view, name=Urls.PROFILE.value),
]
