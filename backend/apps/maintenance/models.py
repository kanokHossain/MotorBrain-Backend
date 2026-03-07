"""
Maintenance models for MotorBrain.

Tracks vehicle maintenance history and reminder schedules.
"""

from django.db import models
from django.conf import settings


class MaintenanceCategory(models.Model):
    """
    Predefined or user-created categories for maintenance parts.
    e.g. Engine Oil, Tyres, Brake Shoes, Battery, etc.
    """

    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True, help_text="Icon identifier for the mobile app")
    is_system = models.BooleanField(default=True, help_text="System-defined categories cannot be deleted")

    class Meta:
        verbose_name = "Maintenance Category"
        verbose_name_plural = "Maintenance Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class MaintenanceRecord(models.Model):
    """
    A single maintenance event for a vehicle.
    Stores part details, cost, service date, and odometer reading.
    """

    vehicle = models.ForeignKey(
        "vehicles.Vehicle",
        on_delete=models.CASCADE,
        related_name="maintenance_records",
    )
    category = models.ForeignKey(
        MaintenanceCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="records",
    )

    part_name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    service_date = models.DateField()
    odometer_km = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    receipt_image = models.ImageField(upload_to="maintenance/receipts/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Maintenance Record"
        verbose_name_plural = "Maintenance Records"
        ordering = ["-service_date", "-odometer_km"]

    def __str__(self):
        return f"{self.vehicle} — {self.part_name} on {self.service_date}"


class MaintenanceReminder(models.Model):
    """
    A scheduled reminder for upcoming vehicle maintenance.
    Can trigger based on time interval (days) or mileage interval (km).
    """

    class TriggerType(models.TextChoices):
        TIME = "time", "Time Interval"
        MILEAGE = "mileage", "Mileage Interval"
        BOTH = "both", "Time and Mileage"

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        DISMISSED = "dismissed", "Dismissed"
        COMPLETED = "completed", "Completed"
        SNOOZED = "snoozed", "Snoozed"

    vehicle = models.ForeignKey(
        "vehicles.Vehicle",
        on_delete=models.CASCADE,
        related_name="maintenance_reminders",
    )
    category = models.ForeignKey(
        MaintenanceCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    last_record = models.ForeignKey(
        MaintenanceRecord,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The maintenance record this reminder is based on",
    )

    name = models.CharField(max_length=200)
    trigger_type = models.CharField(max_length=20, choices=TriggerType.choices, default=TriggerType.BOTH)

    # Time-based trigger
    interval_days = models.PositiveIntegerField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)

    # Mileage-based trigger
    interval_km = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    due_odometer_km = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    notification_sent = models.BooleanField(default=False)
    snoozed_until = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Maintenance Reminder"
        verbose_name_plural = "Maintenance Reminders"
        ordering = ["due_date", "due_odometer_km"]

    def __str__(self):
        return f"{self.vehicle} — {self.name} reminder"
