import random
import string
import hashlib
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.utils.module_loading import import_string
from apps.accounts.models import OTPRequest

def generate_otp(length=6):
    return "".join(random.choices(string.digits, k=length))

def hash_otp(otp):
    return hashlib.sha256(otp.encode()).hexdigest()

def get_otp_provider():
    provider_class = import_string(settings.OTP_PROVIDER_PATH)
    return provider_class()

def create_otp_request(phone_number, purpose, user=None, ip=None, user_agent=None):
    plain_otp = generate_otp()
    otp_hash = hash_otp(plain_otp)
    
    expires_at = timezone.now() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
    request_id = hashlib.md5(f"{phone_number}{timezone.now().timestamp()}".encode()).hexdigest()
    
    otp_request = OTPRequest.objects.create(
        user=user,
        phone_number=phone_number,
        purpose=purpose,
        otp_hash=otp_hash,
        expires_at=expires_at,
        max_attempts=settings.OTP_MAX_ATTEMPTS,
        request_ip=ip,
        user_agent=user_agent,
        request_id=request_id
    )
    
    return otp_request, plain_otp

def send_otp(otp_request, plain_otp):
    provider = get_otp_provider()
    success = provider.send(otp_request, plain_otp)
    if success:
        otp_request.delivery_status = "sent"
    else:
        otp_request.delivery_status = "failed"
    otp_request.save()
    return success

def verify_otp(phone_number, otp, purpose):
    otp_request = OTPRequest.objects.filter(
        phone_number=phone_number,
        purpose=purpose,
        is_used=False,
        expires_at__gt=timezone.now()
    ).first()
    
    if not otp_request:
        return False, "OTP expired or invalid."
    
    if otp_request.attempts >= otp_request.max_attempts:
        return False, "Maximum attempts reached."
    
    otp_request.attempts += 1
    otp_request.save()
    
    if hash_otp(otp) == otp_request.otp_hash:
        otp_request.is_used = True
        otp_request.save()
        
        # Mark console event as verified if it exists
        if hasattr(otp_request, "console_event"):
            otp_request.console_event.is_verified = True
            otp_request.console_event.save()
            
        return True, "OTP verified successfully."
    
    return False, "Invalid OTP."

def can_resend_otp(phone_number, purpose):
    last_request = OTPRequest.objects.filter(
        phone_number=phone_number,
        purpose=purpose
    ).first()
    
    if not last_request:
        return True, 0
    
    cooldown = settings.OTP_RESEND_COOLDOWN_SECONDS
    elapsed = (timezone.now() - last_request.created_at).total_seconds()
    
    if elapsed < cooldown:
        return False, int(cooldown - elapsed)
    
    return True, 0
