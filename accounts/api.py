from rest_framework import viewsets, permissions, exceptions, mixins, views, status
from accounts.serializers import (
    UserDetailSerializer,
    UserListSerializer,
    TransactionSerializer,
    WalletSerializer,
    UserLoginSerializer,
    UserSignupSerializer,
    ChangePasswordSerializer,
    ChangeEmailSerializer,
    EmailVerifySerializer,
)
from django.contrib.auth import authenticate
from rest_framework.response import Response
from utils.constants import LookupFields
from utils.base_utils import get_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    UpdateAPIView,
    RetrieveAPIView,
)
from accounts.constants import AuthResponse, AuthExceptions
from utils.auth_service import AuthService

User = get_model("accounts", "User")
Wallet = get_model("accounts", "Wallet")
Transaction = get_model("accounts", "Transaction")


class UserRegisterationApi(CreateAPIView, GenericAPIView):
    """User Registration API View"""

    permission_classes = [permissions.AllowAny]
    serializer_class = UserSignupSerializer

    def create(self, request, *args, **kwargs):
        instance = super().create(request, *args, **kwargs)
        return Response(
            {"message": AuthResponse.USER_REGISTERED, "data": instance.data},
            status=status.HTTP_201_CREATED,
        )


user_registeration = UserRegisterationApi.as_view()


class UserLoginApi(GenericAPIView):
    """Handle Post Requests to Login User"""

    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer
    auth_service = AuthService()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)
        if not user:
            raise exceptions.ValidationError(AuthExceptions.INVALID_CREDENTIALS)
        return Response(
            self.auth_service.get_auth_tokens_for_user(user=user),
            status=status.HTTP_200_OK,
        )


user_login = UserLoginApi.as_view()


class LogoutApiView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            raise Response(data={"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileApiView(UpdateAPIView, RetrieveAPIView):
    """User Profile API View - Reterive, Update"""

    permission_classes = (IsAuthenticated,)
    serializer_class = UserDetailSerializer
    lookup_field = LookupFields.USERNAME.value

    def get_object(self):
        return self.request.user


user_profile = UserProfileApiView.as_view()


class ChangePasswordApiView(UpdateAPIView, GenericAPIView):
    """Change Password API View - Update"""

    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
    lookup_field = LookupFields.USERNAME.value

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(
            instance, data=request.data, context={"request": request}, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


user_password_change = ChangePasswordApiView.as_view()


class ChangeEmailApiView(UpdateAPIView, GenericAPIView):
    """Change Email API View - Update"""

    permission_classes = (IsAuthenticated,)
    serializer_class = ChangeEmailSerializer

    def get_object(self):
        return self.request.user


user_email_change = ChangeEmailApiView.as_view()


class EmailVerifyApiView(UpdateAPIView, CreateAPIView, GenericAPIView):
    """Email Verify API View - Update"""

    permission_classes = (IsAuthenticated,)
    serializer_class = EmailVerifySerializer

    def create(self, *args, **kwargs):
        """Send Email Verification OTP"""
        # generate_otp.delay(self.request.user.id)
        try:
            return Response(
                {"message": AuthResponse.OTP_GENERATED}, status=status.HTTP_200_OK
            )
        except Exception as err:
            raise Response(
                {
                    "message": AuthExceptions.FAILED_TO_GENERATE_OTP.format(err=err),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def patch(self, request, *args, **kwargs):
        """Verify User Email"""
        serializer = self.serializer_class(
            instance=request.user, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": AuthResponse.EMAIL_VERIFIED},
            status=status.HTTP_200_OK,
        )


email_verify = EmailVerifyApiView.as_view()


class UserViewset(viewsets.ModelViewSet):
    """User Viewset for User CRUD Operations"""

    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    list_serializer_class = UserListSerializer
    detail_serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = LookupFields.USERNAME.value

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        elif self.action == "retrieve":
            return self.detail_serializer_class
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        """Method Not Allowed Since Using Signup API View for Registration"""
        raise exceptions.MethodNotAllowed()


class WalletViewset(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    lookup_field = LookupFields.USER_USERNAME.value
    lookup_url_kwarg = LookupFields.USERNAME.value


class TransactionViewset(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
