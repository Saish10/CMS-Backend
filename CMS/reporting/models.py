from django.db import models
from CMS.utils import BaseModel, ULIDField
from django.utils.translation import gettext_lazy as _


class OutgoingEmail(BaseModel):
    EMAIL_STATUS = [
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    ]
    internal_id = ULIDField(_("outgoing email id"), editable=False)
    from_email = models.EmailField(null=True)
    to_emails = models.CharField(_("to emails"), null=True)
    cc_emails = models.CharField(_("cc emails"), null=True)
    bcc_emails = models.CharField(_("bcc emails"), null=True)
    subject = models.TextField(_("subject"), null=True)
    content = models.TextField(_("content"), null=True)
    status = models.CharField(_("status"), max_length=7, choices=EMAIL_STATUS)

    class Meta:
        verbose_name = "Outgoing Email"
        verbose_name_plural = "Outgoing Emails"


class OutgoingEmailAttachment(BaseModel):
    outgoing_email = models.ForeignKey(
        OutgoingEmail, on_delete=models.CASCADE, related_name="attachments"
    )
    file = models.BinaryField(_("attachment file"))
    filename = models.CharField(_("filename"), max_length=255)

    class Meta:
        verbose_name = "Outgoing Email Attachment"
        verbose_name_plural = "Outgoing Email Attachments"


class Notification(BaseModel):
    NOTIFICATION_LEVEL_CHOICES = [
        ("success", "Success"),
        ("info", "Info"),
        ("warning", "Warning"),
        ("error", "Error"),
    ]
    internal_id = ULIDField(_("notification id"), editable=False)
    level = models.CharField(
        _("level"), max_length=7, choices=NOTIFICATION_LEVEL_CHOICES
    )
    recipient_id = models.CharField(_("recipient ids"))
    is_read = models.BooleanField(default=False)
    subject = models.TextField(
        _("subject"),
    )
    description = models.TextField(_("description"))

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"


class Report(BaseModel):
    REPORT_STATUS = [
        ("processing", "Processing"),
        ("success", "Success"),
        ("failed", "Failed"),
    ]
    internal_id = ULIDField(_("report id"), editable=False)
    user = models.ForeignKey(_("user"))
    tenant = models.ForeignKey(_("tenant"))
    file_name = models.CharField(_("file name"), max_length=10)
    report_name = models.CharField(_("report name"))
    status = models.CharField(
        _("status"), max_length=10, choices=REPORT_STATUS
    )
    format = models.CharField(_("format"), max_length=5)

    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reports"
