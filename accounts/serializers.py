from accounts.models import User, Wallet, Transaction
from utils.base_serializer import (
    DynamicModelSerializer,
)
from rest_framework import serializers
from rest_framework_nested import relations


class UserDetailSerializer(DynamicModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "image",
            "username",
            "email",
            "first_name",
            "last_name",
            "type",
            "age",
            "gender",
            "address",
            "phone",
        ]


class UserListSerializer(DynamicModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        read_only=True,
        view_name="users-detail",
        lookup_field="username",
    )
    wallet = relations.NestedHyperlinkedIdentityField(
        read_only=True, view_name="wallet-detail", lookup_field="username"
    )

    class Meta:
        model = User
        fields = ["id", "url", "username", "get_full_name", "email", "image", "wallet"]


class WalletSerializer(DynamicModelSerializer):

    class Meta:
        model = Wallet
        fields = [
            "id",
            "url",
            "user",
            "balance",
            "created",
            "modified",
        ]


class TransactionSerializer(DynamicModelSerializer):

    class Meta:
        model = Transaction
        fields = ["id", "url", "user", "amount", "type", "description", "created"]
