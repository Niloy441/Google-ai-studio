from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, PhoneForm, OTPVerifyForm
from .models import User
from apps.common.services import create_otp_request, send_otp, verify_otp, can_resend_otp

class SignupPhoneView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, "accounts/signup.html", {"form": form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            full_name = form.cleaned_data["full_name"]
            
            # Store in session temporarily
            request.session["signup_phone"] = phone_number
            request.session["signup_full_name"] = full_name
            
            can_resend, wait_time = can_resend_otp(phone_number, "signup")
            if not can_resend:
                messages.error(request, f"Please wait {wait_time} seconds before requesting another OTP.")
                return render(request, "accounts/signup.html", {"form": form})

            otp_req, plain_otp = create_otp_request(
                phone_number, "signup", 
                ip=request.META.get("REMOTE_ADDR"),
                user_agent=request.META.get("HTTP_USER_AGENT")
            )
            send_otp(otp_req, plain_otp)
            
            return redirect("verify_signup")
        return render(request, "accounts/signup.html", {"form": form})

class VerifySignupOTPView(View):
    def get(self, request):
        phone = request.session.get("signup_phone")
        if not phone:
            return redirect("signup")
        form = OTPVerifyForm()
        return render(request, "accounts/verify_otp.html", {"form": form, "phone": phone, "purpose": "Signup"})

    def post(self, request):
        phone = request.session.get("signup_phone")
        full_name = request.session.get("signup_full_name")
        if not phone:
            return redirect("signup")
            
        form = OTPVerifyForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data["otp"]
            success, msg = verify_otp(phone, otp, "signup")
            if success:
                user = User.objects.create_user(phone_number=phone, full_name=full_name)
                user.is_phone_verified = True
                user.save()
                login(request, user)
                del request.session["signup_phone"]
                del request.session["signup_full_name"]
                messages.success(request, "Account created successfully!")
                return redirect("profile")
            else:
                messages.error(request, msg)
        return render(request, "accounts/verify_otp.html", {"form": form, "phone": phone, "purpose": "Signup"})

class LoginPhoneView(View):
    def get(self, request):
        form = PhoneForm()
        return render(request, "accounts/login.html", {"form": form})

    def post(self, request):
        form = PhoneForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            user = User.objects.filter(phone_number=phone_number).first()
            
            if not user:
                messages.error(request, "No account found with this phone number.")
                return render(request, "accounts/login.html", {"form": form})
            
            request.session["login_phone"] = phone_number
            
            can_resend, wait_time = can_resend_otp(phone_number, "login")
            if not can_resend:
                messages.error(request, f"Please wait {wait_time} seconds before requesting another OTP.")
                return render(request, "accounts/login.html", {"form": form})

            otp_req, plain_otp = create_otp_request(
                phone_number, "login", user=user,
                ip=request.META.get("REMOTE_ADDR"),
                user_agent=request.META.get("HTTP_USER_AGENT")
            )
            send_otp(otp_req, plain_otp)
            
            return redirect("verify_login")
        return render(request, "accounts/login.html", {"form": form})

class VerifyLoginOTPView(View):
    def get(self, request):
        phone = request.session.get("login_phone")
        if not phone:
            return redirect("login")
        form = OTPVerifyForm()
        return render(request, "accounts/verify_otp.html", {"form": form, "phone": phone, "purpose": "Login"})

    def post(self, request):
        phone = request.session.get("login_phone")
        if not phone:
            return redirect("login")
            
        form = OTPVerifyForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data["otp"]
            success, msg = verify_otp(phone, otp, "login")
            if success:
                user = User.objects.get(phone_number=phone)
                login(request, user)
                del request.session["login_phone"]
                messages.success(request, "Logged in successfully!")
                return redirect("profile")
            else:
                messages.error(request, msg)
        return render(request, "accounts/verify_otp.html", {"form": form, "phone": phone, "purpose": "Login"})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")

class ProfileView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, "accounts/profile.html", {"user": request.user})
