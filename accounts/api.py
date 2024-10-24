from rest_framework import viewsets, permissions, exceptions, mixins, views, status
from accounts.serializers import (
    UserDetailSerializer,
    UserListSerializer,
    TransactionSerializer,
    WalletSerializer,
    UserLoginSerializer,
    UserSignupSerializer,
)
from django.contrib.auth import authenticate
from rest_framework.response import Response
from utils.constants import AccountsViews, LookupFields
from utils.base_utils import get_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

User = get_model("accounts", "User")
Wallet = get_model("accounts", "Wallet")
Transaction = get_model("accounts", "Transaction")


class LoggedInUser(views.APIView):
    """Logged in User Serializer"""

    def get(self, request, *args, **kwargs):
        """returns authenticated user details"""
        if request.user.is_authenticated:
            serializer = UserListSerializer(request.user, context={"request": request})
            return Response(serializer.data)
        raise Response(
            data={"message": AccountsViews.USER_NOT_AUTHENTICATED.value},
            status=status.HTTP_401_UNAUTHORIZED,
        )


logged_in_user = LoggedInUser.as_view()


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


class UserRegistrationApiView(views.APIView):
    """User Registration API View"""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data["password"]
            try:
                user = serializer.create(serializer.validated_data)
                user.set_password(password)
                user.save()
                return Response(
                    data={"message": AccountsViews.REGISTRATION_SUCCESS.value},
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                raise Response(
                    data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        raise Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(views.APIView):
    """Handle Post Requests to Login User"""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(request, username=username, password=password)

            if user:
                refresh = RefreshToken.for_user(user)

                return Response(
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                raise Response(
                    {"message": AccountsViews.INVALID_CREDENTIALS.value},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        raise Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
