from django.test import TestCase, Client
from django.urls import reverse
from apps.accounts.models import User, OTPRequest
from apps.common.services import create_otp_request, hash_otp

class OTPAuthTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.phone = "+1234567890"
        self.full_name = "Test User"

    def test_signup_flow_starts(self):
        response = self.client.post(reverse("signup"), {
            "phone_number": self.phone,
            "full_name": self.full_name
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(OTPRequest.objects.count(), 1)
        self.assertEqual(self.client.session["signup_phone"], self.phone)

    def test_otp_verification_success(self):
        # Setup session
        session = self.client.session
        session["signup_phone"] = self.phone
        session["signup_full_name"] = self.full_name
        session.save()

        # Create OTP
        otp_req, plain_otp = create_otp_request(self.phone, "signup")
        
        response = self.client.post(reverse("verify_signup"), {
            "otp": plain_otp
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(phone_number=self.phone).exists())
        user = User.objects.get(phone_number=self.phone)
        self.assertTrue(user.is_phone_verified)

    def test_otp_verification_failure(self):
        session = self.client.session
        session["signup_phone"] = self.phone
        session.save()

        create_otp_request(self.phone, "signup")
        
        response = self.client.post(reverse("verify_signup"), {
            "otp": "000000" # Wrong OTP
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(phone_number=self.phone).exists())
