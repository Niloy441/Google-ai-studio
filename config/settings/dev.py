from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

# Email backend for dev
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Internal Console OTP Provider is default for dev
OTP_PROVIDER = "apps.common.otp_providers.InternalConsoleOTPProvider"
