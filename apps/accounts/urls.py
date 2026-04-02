from django.urls import path
from .views import (
    SignupPhoneView, VerifySignupOTPView, 
    LoginPhoneView, VerifyLoginOTPView, 
    LogoutView, ProfileView
)

urlpatterns = [
    path("signup/", SignupPhoneView.as_view(), name="signup"),
    path("signup/verify/", VerifySignupOTPView.as_view(), name="verify_signup"),
    path("login/", LoginPhoneView.as_view(), name="login"),
    path("login/verify/", VerifyLoginOTPView.as_view(), name="verify_login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("", LoginPhoneView.as_view(), name="home"),
]
