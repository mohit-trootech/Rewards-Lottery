from django.urls import path, include
from django.contrib import admin
from accounts.api import (
    UserViewset,
    WalletViewset,
    TransactionViewset,
)
from rest_framework import routers
from debug_toolbar.toolbar import debug_toolbar_urls
from schema_graph.views import Schema
from utils.constants import Urls, BaseNames, AppNames
from django.conf import settings
from django.conf.urls.static import static
from rewards.views import (
    LotterViewset,
    WinnerViewset,
    BuyerViewset,
    OrderViewset,
)

app_name = AppNames.REWARDS.value


# Router
router = routers.DefaultRouter()
router.register("users", UserViewset, basename=BaseNames.USERS.value)
router.register("wallet", WalletViewset, basename=BaseNames.WALLET.value)
router.register("transaction", TransactionViewset, basename=BaseNames.TRANSACTION.value)
router.register("lotteries", LotterViewset, basename=BaseNames.LOTTERIES.value)
router.register("winners", WinnerViewset, basename=BaseNames.WINNERS.value)
router.register("buyers", BuyerViewset, basename=BaseNames.BUYERS.value)
router.register("orders", OrderViewset, basename=BaseNames.ORDERS.value)

# Urlspatterns
urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("api/", include(router.urls), name=Urls.API_ROOT.value),
    path("schema/", Schema.as_view(), name=Urls.SCHEMA_REVERSE.value),
    path("demo/", include("demo.urls")),
] + debug_toolbar_urls()

urlpatterns = urlpatterns + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
