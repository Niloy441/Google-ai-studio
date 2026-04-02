from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.conf import settings
from .models import OTPConsoleEvent, OTPAuditLog
from .forms import ConsoleLoginForm

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

class ConsoleLoginView(LoginView):
    template_name = "console/login.html"
    authentication_form = ConsoleLoginForm
    
    def get_success_url(self):
        return "/console/dashboard/"

class ConsoleDashboardView(AdminRequiredMixin, View):
    def get(self, request):
        recent_events = OTPConsoleEvent.objects.all()[:10]
        return render(request, "console/dashboard.html", {"events": recent_events})

class OTPEventListView(AdminRequiredMixin, View):
    def get(self, request):
        phone = request.GET.get("phone")
        events = OTPConsoleEvent.objects.all()
        if phone:
            events = events.filter(otp_request__phone_number__icontains=phone)
        return render(request, "console/otp_event_list.html", {"events": events})

class OTPEventDetailView(AdminRequiredMixin, View):
    def get(self, request, pk):
        event = get_object_or_404(OTPConsoleEvent, pk=pk)
        
        # Record audit log
        OTPAuditLog.objects.create(
            admin_user=request.user,
            event=event,
            action="viewed_otp",
            ip_address=request.META.get("REMOTE_ADDR")
        )
        
        show_otp = settings.DEBUG # Only show plain OTP in dev mode
        
        return render(request, "console/otp_event_detail.html", {
            "event": event,
            "show_otp": show_otp
        })
