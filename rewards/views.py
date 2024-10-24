from rest_framework import permissions, parsers, viewsets, mixins
from rewards.serializers import (
    LotteryListSerializer,
    LotteryDetailSerializer,
    WinnerSerializer,
    BuyerSerializer,
    OrderSerializer,
)
from django.db.models import Q
from django_extensions.db.models import ActivatorModel
from utils.viewsets import SoftDestroyModelViewset
from utils.base_utils import get_model
from utils.pagination import StandardPagination

Lottery = get_model("rewards", "Lottery")
Winner = get_model("rewards", "Winner")
Buyer = get_model("rewards", "Buyer")
Order = get_model("rewards", "Order")


class LotterViewset(SoftDestroyModelViewset):
    queryset = Lottery.objects.all()
    serializer_class = LotteryDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    pagination_class = StandardPagination

    def get_serializer_class(self):
        if self.action == "list":
            return LotteryListSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        query = Q(title__icontains=self.request.query_params.get("q", "")) & Q(
            status=ActivatorModel.ACTIVE_STATUS
        )

        return (
            super()
            .get_queryset()
            .filter(query)
            .order_by(
                self.request.query_params.get("sort", "?"),
                self.request.query_params.get("price", "?"),
            )
        )


class WinnerViewset(SoftDestroyModelViewset):
    queryset = Winner.objects.all()
    serializer_class = WinnerSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class BuyerViewset(SoftDestroyModelViewset):
    serializer_class = BuyerSerializer
    queryset = Buyer.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        from django.db.models import Q

        query = Q()
        if "user" in self.request.query_params:
            query = query & Q(
                user__username__icontains=self.request.query_params.get("user")
            )
        return super().get_queryset().filter(query)


class OrderViewset(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """Order Models API Viewset"""

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
