from abc import ABC, abstractmethod
import logging
from django.conf import settings
from apps.console.models import OTPConsoleEvent

logger = logging.getLogger(__name__)

class BaseOTPProvider(ABC):
    @abstractmethod
    def send(self, otp_request, plain_otp):
        pass

class InternalConsoleOTPProvider(BaseOTPProvider):
    """
    Development provider that saves OTP to a console event instead of sending SMS.
    """
    def send(self, otp_request, plain_otp):
        OTPConsoleEvent.objects.create(
            otp_request=otp_request,
            plain_otp=plain_otp
        )
        logger.info(f"OTP for {otp_request.phone_number} saved to internal console.")
        return True

class SMSOTPProvider(BaseOTPProvider):
    """
    Production provider stub for SMS.
    """
    def send(self, otp_request, plain_otp):
        # In production, integrate with Twilio, MessageBird, etc.
        logger.info(f"SMS would be sent to {otp_request.phone_number} in production.")
        # For now, we just log it (don't log plain_otp in real production!)
        return True
