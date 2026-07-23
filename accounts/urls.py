from django.urls import path

from accounts.views.account import AccountMeView
from accounts.views.login import LoginView
from accounts.views.logout import LogoutView
from accounts.views.otp import ResendOTPView, VerifyOTPView
from accounts.views.profile import ProfileMeView
from accounts.views.register import RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path("resend-otp/", ResendOTPView.as_view(), name="resend-otp"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("me/", AccountMeView.as_view(), name="account-me"),
    path("me/profile/", ProfileMeView.as_view(), name="profile-me"),
]
