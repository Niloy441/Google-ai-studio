import uuid
from django.db import models
from django.conf import settings

class OTPConsoleEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    otp_request = models.OneToOneField("accounts.OTPRequest", on_delete=models.CASCADE, related_name="console_event")
    plain_otp = models.CharField(max_length=6, help_only="Only visible in dev mode")
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

class OTPAuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    admin_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    event = models.ForeignKey(OTPConsoleEvent, on_delete=models.CASCADE, related_name="audit_logs")
    action = models.CharField(max_length=50) # e.g., "viewed_otp"
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ["-timestamp"]
