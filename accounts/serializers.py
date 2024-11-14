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
from accounts.constants import ValidationErrors, Choices
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist

User = get_model("accounts", "User")
Wallet = get_model("accounts", "Wallet")
Transaction = get_model("accounts", "Transaction")
Otp = get_model("accounts", "Otp")


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
            "is_verified",
            "date_joined",
            "last_login",
        ]
        depth = True

    def validate_age(self, value):
        if value < 18:
            raise serializers.ValidationError(ValidationErrors.INVALID_AGE)
        return value


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(
        write_only=True, validators=[password_strength]
    )
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        user = self.context["request"].user
        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError(
                {"old_password": ValidationErrors.INVALID_PASSWORD}
            )
        if attrs["new_password"] == attrs["old_password"]:
            raise serializers.ValidationError(
                {"new_password": ValidationErrors.SAME_PASSWORD}
            )
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": ValidationErrors.UNMATCHED_PASSWORDS}
            )
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get("new_password"))
        instance.save()
        return instance


class ChangeEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
        ]

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.is_verified = False
        instance.save(update_fields=["is_verified"])
        return instance


class EmailVerifySerializer(serializers.ModelSerializer):
    """Email Verification Serializer"""

    class Meta:
        model = Otp
        fields = ["otp"]

    def validate_otp(self, value):
        """Validate OTP"""
        # Check it OTP Expired

        user = self.context["request"].user
        try:
            if user.otp.otp != value:
                """Check if OTP is Validated"""
                raise serializers.ValidationError(
                    {"otp": [ValidationErrors.INVALID_OTP]}
                )
            if user.otp.expiry < now():
                """If Expiry Date if Smaller Than Current Datetime Means OTP is Expired Hence Raise OTP Expiry Validation Error"""
                raise serializers.ValidationError(
                    {"otp": [ValidationErrors.OTP_EXPIRED]}
                )
            return value
        except ObjectDoesNotExist:
            raise serializers.ValidationError(ValidationErrors.OTP_NOT_FOUND)

    def update(self, instance, validated_data):
        """Update User Email"""
        instance.otp.delete()
        instance.is_verified = Choices.ACTIVE_STATUS
        instance.save(update_fields=["is_verified"])
        return instance


class TransactionSerializer(DynamicModelSerializer):
    user = UserListSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ["id", "user", "amount", "option", "created", "description"]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs["user"] = User.objects.get(pk=self.initial_data["user"])
        return attrs
