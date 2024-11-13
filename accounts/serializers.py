from utils.base_serializer import (
    DynamicModelSerializer,
)
from rest_framework import serializers
from django.contrib.auth.password_validation import (
    validate_password as password_strength,
)
from utils.base_utils import get_model
from email_validator import validate_email as validate_email_validator
from email_validator import EmailNotValidError
from accounts.constants import ValidationErrors

User = get_model("accounts", "User")
Wallet = get_model("accounts", "Wallet")
Transaction = get_model("accounts", "Transaction")


class UserSignupSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True, write_only=True)
    age = serializers.IntegerField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "option",
            "confirm_password",
            "email",
            "age",
        ]
        extra_kwargs = {
            "password": {"write_only": True, "validators": [password_strength]},
        }

    def validate_email(self, value):
        """Check Whether the Email is a Valid Email or Not"""
        try:
            validate_email_validator(value)
        except EmailNotValidError as eve:
            raise serializers.ValidationError(str(eve))
        return value

    def validate_age(self, value):
        """validate user age for signup"""
        if value < 18:
            raise serializers.ValidationError(ValidationErrors.INVALID_AGE)
        return value

    def validate(self, attrs):
        """validate password and confirm password"""
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": ValidationErrors.UNMATCHED_PASSWORDS}
            )
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("confirm_password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


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
            raise serializers.ValidationError(ValidationErrors.INVALID_AGE)
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
