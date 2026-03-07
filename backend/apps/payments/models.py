"""
Payment models for MotorBrain.

Tracks subscription payments and transaction history.
"""

from django.db import models
from django.conf import settings


class Payment(models.Model):
    """
    A subscription payment transaction.
    """

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"
        REFUNDED = "refunded", "Refunded"

    class Currency(models.TextChoices):
        USD = "USD", "USD"
        EUR = "EUR", "EUR"
        BDT = "BDT", "BDT"
        GBP = "GBP", "GBP"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=5, choices=Currency.choices, default=Currency.USD)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    plan = models.CharField(max_length=50, help_text="Subscription plan purchased")
    payment_provider = models.CharField(max_length=100, blank=True, help_text="e.g. Stripe, bKash")
    transaction_id = models.CharField(max_length=255, blank=True, unique=True)
    receipt_url = models.URLField(blank=True)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} — {self.amount} {self.currency} ({self.status})"
