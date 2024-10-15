from django.urls import path, include
from django.contrib import admin
from accounts.views import UserViewset, WalletViewset, TransactionViewset
from rest_framework import routers
from debug_toolbar.toolbar import debug_toolbar_urls
from schema_graph.views import Schema
from utils.constants import Urls
from django.conf import settings
from django.conf.urls.static import static


router = routers.DefaultRouter()
router.register("users", UserViewset, basename="users")
router.register("wallets", WalletViewset, basename="wallets")
router.register("transactions", TransactionViewset, basename="transaction")
app_name = "rewards"
urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("api/", include(router.urls), name=Urls.API_ROOT.value),
    path("schema/", Schema.as_view(), name=Urls.SCHEMA_REVERSE.value),
] + debug_toolbar_urls()

urlpatterns = urlpatterns + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
