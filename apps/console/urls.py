from django.urls import path
from .views import ConsoleLoginView, ConsoleDashboardView, OTPEventListView, OTPEventDetailView

urlpatterns = [
    path("login/", ConsoleLoginView.as_view(), name="console_login"),
    path("dashboard/", ConsoleDashboardView.as_view(), name="console_dashboard"),
    path("otp-events/", OTPEventListView.as_view(), name="console_otp_list"),
    path("otp-events/<uuid:pk>/", OTPEventDetailView.as_view(), name="console_otp_detail"),
    path("", ConsoleDashboardView.as_view()),
]
