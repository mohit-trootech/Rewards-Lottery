from django.views.generic import TemplateView


class DemoHome(TemplateView):
    template_name = "demo/home.html"


demo_home = DemoHome.as_view()


class CreateLottery(TemplateView):
    template_name = "demo/create.html"


create_lottery = CreateLottery.as_view()


class DetailLottery(TemplateView):
    template_name = "demo/detail.html"


detail_lottery = DetailLottery.as_view()


class PurchaseLottery(TemplateView):
    template_name = "demo/purchase.html"


purchase_lottery = PurchaseLottery.as_view()


class TransactionsView(TemplateView):
    template_name = "demo/transactions.html"


transactions_view = TransactionsView.as_view()


class WiningView(TemplateView):
    template_name = "demo/winning.html"


winning_view = WiningView.as_view()


class SignupView(TemplateView):
    template_name = "accounts/signup.html"


signup_view = SignupView.as_view()


class LoginView(TemplateView):
    template_name = "accounts/login.html"


login_view = LoginView.as_view()


class ProfileView(TemplateView):
    template_name = "accounts/profile.html"


profile_view = ProfileView.as_view()


class ForgotPasswordView(TemplateView):
    template_name = "accounts/forgot_password.html"


forgot_password_view = ForgotPasswordView.as_view()


class ResetPasswordView(TemplateView):
    template_name = "accounts/reset_password.html"


reset_password_view = ResetPasswordView.as_view()
