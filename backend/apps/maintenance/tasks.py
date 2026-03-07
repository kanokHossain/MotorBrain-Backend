"""
Celery tasks for maintenance reminders.
"""

from celery import shared_task
from django.utils import timezone
from datetime import date


@shared_task
def check_maintenance_reminders():
    """
    Periodic task: check all active reminders and send push notifications
    for those that are due based on time or mileage.
    """
    from .models import MaintenanceReminder
    from apps.notifications.models import Notification

    today = date.today()
    due_reminders = MaintenanceReminder.objects.filter(
        status="active",
        notification_sent=False,
    ).select_related("vehicle", "vehicle__owner", "category")

    sent_count = 0
    for reminder in due_reminders:
        is_due = False

        if reminder.due_date and reminder.due_date <= today:
            is_due = True

        current_odometer = reminder.vehicle.current_odometer_km
        if reminder.due_odometer_km and current_odometer >= reminder.due_odometer_km:
            is_due = True

        if is_due:
            Notification.objects.create(
                user=reminder.vehicle.owner,
                vehicle=reminder.vehicle,
                notification_type="maintenance_reminder",
                title=f"Maintenance Due: {reminder.name}",
                body=(
                    f"Your {reminder.vehicle.name} is due for {reminder.name}. "
                    "Check the app for details."
                ),
                data={"reminder_id": reminder.id, "vehicle_id": reminder.vehicle.id},
            )
            reminder.notification_sent = True
            reminder.save(update_fields=["notification_sent"])
            sent_count += 1

    return f"Sent {sent_count} maintenance reminder notifications."
