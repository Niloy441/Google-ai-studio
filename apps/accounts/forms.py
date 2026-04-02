from django import forms
from django.core.exceptions import ValidationError
import phonenumbers
from .models import User

class PhoneForm(forms.Form):
    phone_number = forms.CharField(
        max_length=20, 
        widget=forms.TextInput(attrs={
            "placeholder": "+1234567890",
            "type": "tel"
        }),
        help_text="Include your country code starting with '+' (e.g., +1 for USA)."
    )
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")
        if not phone.startswith('+'):
            raise ValidationError("Phone number must start with a '+' followed by the country code.")
            
        try:
            parsed = phonenumbers.parse(phone, None)
            if not phonenumbers.is_valid_number(parsed):
                raise ValidationError("The phone number entered is not a valid international number.")
            return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        except phonenumbers.NumberParseException:
            raise ValidationError("Please enter a valid phone number in international format (e.g., +1234567890).")

class SignupForm(PhoneForm):
    full_name = forms.CharField(max_length=150)
    
    def clean_phone_number(self):
        phone = super().clean_phone_number()
        if User.objects.filter(phone_number=phone).exists():
            raise ValidationError("A user with this phone number already exists.")
        return phone

class OTPVerifyForm(forms.Form):
    otp = forms.CharField(min_length=6, max_length=6, widget=forms.TextInput(attrs={"autocomplete": "one-time-code"}))
