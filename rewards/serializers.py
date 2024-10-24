from rest_framework import serializers
from utils.base_serializer import DynamicModelSerializer
from accounts.serializers import UserListSerializer, TransactionSerializer
from utils.constants import (
    LookupFields,
    RewardsSerilizerConstants,
    Choices,
    TransactionDescription,
)
from utils.base_utils import get_model
from utils.utils import (
    get_models_instance_else_serializer_validation_error,
    check_whether_user_can_buy_lottery_else_validation_error,
    check_wallet_minumun_balance_criteria,
    check_user_options,
)

User = get_model("accounts", "User")
Transaction = get_model("accounts", "Transaction")
Lottery = get_model("rewards", "Lottery")
Winner = get_model("rewards", "Winner")
Buyer = get_model("rewards", "Buyer")
Order = get_model("rewards", "Order")


class LotteryListSerializer(DynamicModelSerializer):
    vendor = UserListSerializer(read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name=RewardsSerilizerConstants.LOTTERIES_DETAIL.value,
        lookup_field=LookupFields.SLUG.value,
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

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs["vendor"] = self.context["request"].user
        return attrs

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        query_params = self.context["request"].query_params
        if "buyer" in query_params:
            serializer = BuyerSerializer(
                data={
                    "user": query_params["buyer"],
                    "lottery": instance,
                    "amount": instance.price,
                    "quantity": (
                        query_params.get("quantity")
                        if query_params.get("quantity")
                        else 1
                    ),
                }
            )
            serializer.is_valid(raise_exception=True)
            buyer = serializer.save()
            transaction_serializer = TransactionSerializer(
                data={
                    "user": query_params["buyer"],
                    "amount": buyer.amount,
                    "option": Choices.DEBIT.value,
                    "description": TransactionDescription.LOTTERY_PURCHASE.value,
                }
            )
            transaction_serializer.is_valid(raise_exception=True)
            transaction_serializer.save()
            buyer.user.wallet.balance -= buyer.amount
            buyer.user.wallet.save(update_fields=["balance"])
        return instance


class BuyerWinnerBaseSerializer(DynamicModelSerializer):
    user = UserListSerializer(read_only=True)
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

    def validate_user(self, value):
        """Validate User"""
        breakpoint()
        return value

    def validate(self, attrs):
        """validate whether the user is customer & wallet balance is sufficient or not"""
        try:
            user = get_models_instance_else_serializer_validation_error(
                self.initial_data["user"], User
            )
            check_whether_user_can_buy_lottery_else_validation_error(
                user, attrs["amount"]
            )
            check_wallet_minumun_balance_criteria(user)
            check_user_options(user)
            attrs["user"] = user
            attrs["lottery"] = self.initial_data["lottery"]
        except KeyError as ke:
            raise serializers.ValidationError(str(ke))
        return super().validate(attrs)


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
