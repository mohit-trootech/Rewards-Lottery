from rest_framework import serializers
from utils.base_serializer import DynamicModelSerializer
from accounts.serializers import UserListSerializer, TransactionSerializer
from utils.constants import (
    LookupFields,
    RewardsSerilizerConstants,
    TransactionDescription,
)
from rewards.constants import (
    ValidationErrors,
    SerializerConstants,
    LookUps,
    TransactionDescriptions,
)
from utils.base_utils import get_model
from utils.utils import (
    check_wallet_minumun_balance_criteria,
    check_user_options,
)
from accounts.constants import Choices

User = get_model("accounts", "User")
Transaction = get_model("accounts", "Transaction")
Lottery = get_model("rewards", "Lottery")
Winner = get_model("rewards", "Winner")
Buyer = get_model("rewards", "Buyer")
Order = get_model("rewards", "Order")


class LotteryListSerializer(DynamicModelSerializer):
    vendor = UserListSerializer(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    url = serializers.HyperlinkedIdentityField(
        view_name=SerializerConstants.LOTTERIES_DETAIL,
        lookup_field=LookUps.SLUG,
    )
    buyer_count = serializers.SerializerMethodField(read_only=True)

    def get_buyer_count(self, obj):
        return Buyer.objects.filter(lottery=obj).count()

    class Meta:
        model = Lottery
        fields = [
            "id",
            "url",
            "title",
            "slug",
            "image",
            "status",
            "price",
            "vendor",
            "description",
            "winning",
            "total_draw",
            "expiry_date",
            "created",
            "buyer_count",
        ]
        depth = True


class LotteryDetailSerializer(LotteryListSerializer):
    class Meta(LotteryListSerializer.Meta):
        read_only_fields = ("vendor", "created", "modified")
        fields = (
            "id",
            "title",
            "description",
            "slug",
            "image",
            "status",
            "price",
            "vendor",
            "buyers",
            "created",
            "expiry_date",
            "winning",
            "total_draw",
            "modified",
            "lottery_cash",
        )


class LotteryPurchaseSerializer(serializers.Serializer):
    """Serializer to validate Lottery Purchase"""

    user = serializers.CurrentUserDefault()
    quantity = serializers.IntegerField(default=1)
    lottery = LotteryListSerializer(read_only=True)

    def create(self, validated_data):
        buyer = BuyerSerializer(
            data=validated_data,
            context={"request": self.context["request"]},
        )
        buyer.is_valid(raise_exception=True)
        buyer.save()
        transaction = TransactionSerializer(
            data={
                "user": validated_data["user"].id,
                "amount": buyer.validated_data["amount"],
                "option": Choices.DEBIT,
                "description": TransactionDescriptions.LOTTERY_PURCHASE,
            }
        )
        transaction.is_valid(raise_exception=True)
        transaction.save()
        buyer.user.wallet.balance -= buyer.validated_data["amount"]
        buyer.user.wallet.save(update_fields=["balance"])
        return super().create(validated_data)


class BuyerWinnerBaseSerializer(DynamicModelSerializer):
    user = UserListSerializer(read_only=True, default=serializers.CurrentUserDefault())
    lottery = LotteryListSerializer(read_only=True)


class BuyerSerializer(BuyerWinnerBaseSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name=RewardsSerilizerConstants.BUYERS_DETAIL.value,
        lookup_field=LookupFields.PK.value,
    )

    class Meta:
        model = Buyer
        read_only_fields = ["user", "lottery"]
        fields = [
            "id",
            "user",
            "amount",
            "quantity",
            "lottery",
            "url",
            "created",
            "modified",
        ]
        depth = True

    def validate_amount(self, value):
        """Check amount available to purchase lottery"""
        if value > self.initial_data["lottery"]["price"]:
            raise serializers.ValidationError(ValidationErrors.NOT_ENOUGH_AMOUNT)
        return value

    def validate_user(self, value):
        """Check, user wallet minimum balance & whether user is customer"""
        check_wallet_minumun_balance_criteria(value)
        check_user_options(value)
        return value


class WinnerSerializer(BuyerWinnerBaseSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name=RewardsSerilizerConstants.WINNERS_DETAIL.value,
        lookup_field=RewardsSerilizerConstants.PK.value,
    )

    class Meta:
        model = Winner
        fields = ["id", "url", "user", "lottery", "amount", "created", "modified"]
        depth = True


class OrderSerializer(DynamicModelSerializer):
    user = UserListSerializer(read_only=True)
    transaction = TransactionSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "payer",
            "email",
            "amount",
            "status",
            "transaction",
            "user",
            "created",
            "modified",
        ]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        serializer = TransactionSerializer(
            data={
                "user": self.context["request"].user.id,
                "amount": validated_data["amount"],
                "option": Choices.CREDIT.value,
                "description": TransactionDescription.WALLET_TOPUP.value,
            }
        )
        serializer.is_valid(raise_exception=True)
        validated_data["transaction"] = serializer.save()
        validated_data["user"].wallet.balance += validated_data["amount"]
        validated_data["user"].wallet.save(update_fields=["balance"])
        return super().create(validated_data)
