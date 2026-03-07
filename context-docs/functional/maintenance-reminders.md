# Feature: Maintenance Reminders

## Related Modules
- [Maintenance](../modules/maintenance.md)
- [Vehicles](../modules/vehicles.md)
- [Notifications](../modules/notifications.md)
- [Mileage](../modules/mileage.md)

---

## Feature Description

The system automatically reminds users when their vehicle is due for a maintenance service based on configurable time and/or mileage intervals. Reminders are created by users (manually or suggested by the system after logging maintenance) and processed by a background Celery task.

---

## User Flow

### Creating a Reminder

1. After logging a maintenance record, the app prompts: "Set a reminder for next service?"
2. User confirms and optionally adjusts the interval
3. App sends `POST /api/v1/maintenance/reminders/` with:
   - `vehicle`
   - `name` (e.g. "Engine Oil Change")
   - `trigger_type`: time / mileage / both
   - `interval_days` and/or `interval_km`
4. System computes `due_date` and `due_odometer_km` from the current service date/odometer + intervals

### Receiving a Reminder

1. At the scheduled Celery beat interval (e.g. daily at 9:00 AM)
2. `check_maintenance_reminders` task runs
3. For each active, un-notified reminder:
   - If `due_date <= today` → due by time
   - If `vehicle.current_odometer_km >= due_odometer_km` → due by mileage
4. On any trigger condition:
   - A `Notification` is created
   - Push notification is sent via FCM
   - `notification_sent = True`

### Responding to a Reminder

- **Complete**: User logs the maintenance → reminder status set to `completed`
- **Dismiss**: User dismisses without logging → status set to `dismissed`
- **Snooze**: User snoozes for X days → `snoozed_until` is set, `notification_sent` reset after snooze expires

---

## Business Rules

- A reminder is only triggered once per cycle (`notification_sent` prevents duplicates)
- After snoozing, the notification can be sent again after `snoozed_until`
- When a new maintenance record is logged for the same category and vehicle, any active reminder for that category is auto-completed
- Mileage-based reminders are re-evaluated whenever the vehicle's `current_odometer_km` is updated

---

## System Behavior

The reminder processing task is scheduled via Django Celery Beat and stored in the database. The default schedule is **daily at 9:00 AM UTC**. This can be changed from the Django admin without code changes.
