"""
Notification models for MotorBrain.

Manages in-app notifications and push notification history.
"""

from django.db import models
from django.conf import settings


class Notification(models.Model):
    """
    An in-app notification sent to a user.
    """

    class NotificationType(models.TextChoices):
        MAINTENANCE_REMINDER = "maintenance_reminder", "Maintenance Reminder"
        MILEAGE_THRESHOLD = "mileage_threshold", "Mileage Threshold"
        SUBSCRIPTION = "subscription", "Subscription"
        AI_INSIGHT = "ai_insight", "AI Insight"
        SYSTEM = "system", "System"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    notification_type = models.CharField(
        max_length=50, choices=NotificationType.choices
    )
    title = models.CharField(max_length=255)
    body = models.TextField()
    data = models.JSONField(default=dict, blank=True, help_text="Extra context payload for deep linking")
    is_read = models.BooleanField(default=False)
    push_sent = models.BooleanField(default=False)
    push_sent_at = models.DateTimeField(null=True, blank=True)

    # Optional reference to vehicle or reminder
    vehicle = models.ForeignKey(
        "vehicles.Vehicle",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} — {self.title}"
