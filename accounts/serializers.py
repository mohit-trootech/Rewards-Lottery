from utils.base_serializer import (
    DynamicModelSerializer,
)
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from utils.base_utils import get_model
from utils.constants import AccountsSerilizerConstants

User = get_model("accounts", "User")
Wallet = get_model("accounts", "Wallet")
Transaction = get_model("accounts", "Transaction")


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UserSignupSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)
    age = serializers.IntegerField(required=True)

    class Meta:
        model = User
        fields = ["id", "username", "password", "confirm_password", "email", "age"]

    def validate_age(self, value):
        """validate user age for signup"""
        if value < 18:
            raise serializers.ValidationError(
                AccountsSerilizerConstants.AGE_NOT_VALID.value
            )
        return value

    def validate(self, attrs):
        """validate password and confirm password"""
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def validate_password(self, value):
        """validate password strength"""
        validate_password(value)
        return value

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        return super().create(validated_data)


class UserListSerializer(DynamicModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        read_only=True,
        view_name="users-detail",
        lookup_field="username",
    )

    class Meta:
        model = User
        fields = ["id", "url", "username", "first_name", "last_name", "email", "image"]


class WalletSerializer(DynamicModelSerializer):
    class Meta:
        model = Wallet
        fields = [
            "id",
            "balance",
            "created",
            "modified",
        ]


class UserDetailSerializer(UserListSerializer):
    wallet = WalletSerializer(read_only=True)
    age = serializers.IntegerField(required=True)

    class Meta(UserListSerializer.Meta):
        fields = [
            "id",
            "image",
            "username",
            "email",
            "first_name",
            "last_name",
            "option",
            "age",
            "gender",
            "address",
            "phone",
            "wallet",
        ]
        depth = True

    def validate_age(self, value):
        if value < 18:
            raise serializers.ValidationError(
                AccountsSerilizerConstants.AGE_NOT_VALID.value
            )
        return value


class TransactionSerializer(DynamicModelSerializer):
    user = UserListSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ["id", "user", "amount", "option", "created", "description"]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs["user"] = User.objects.get(pk=self.initial_data["user"])
        return attrs
