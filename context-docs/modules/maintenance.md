# Module: Maintenance

**Django App:** `apps.maintenance`

---

## Purpose

The Maintenance module lets users log all service activities for their vehicles and manages time- and mileage-based reminders for upcoming maintenance.

---

## Responsibilities

- CRUD for maintenance records (part replaced, brand, cost, date, odometer)
- Predefined maintenance categories (Engine Oil, Tyres, Battery, etc.)
- Receipt image storage per maintenance record
- Maintenance reminder scheduling (by days or km interval)
- Triggering push notifications when a reminder is due
- Celery task for periodic reminder evaluation

---

## Models

### `MaintenanceCategory`
Predefined service categories. Examples:
- Engine Oil
- Gearbox Oil
- Brake Shoes
- Tyres
- Battery
- Air Filter
- Fuel Filter
- Chain (for bikes)

### `MaintenanceRecord`
A single maintenance event. Links to a Vehicle and a Category.

Key fields:
- `part_name`, `brand`, `cost`
- `service_date`, `odometer_km`
- `notes`, `receipt_image`

### `MaintenanceReminder`
A scheduled service reminder. Can trigger by time (days), mileage (km), or both.

Key fields:
- `trigger_type` — time | mileage | both
- `interval_days`, `due_date` — time-based fields
- `interval_km`, `due_odometer_km` — mileage-based fields
- `status` — active | dismissed | completed | snoozed
- `notification_sent` — flag to prevent duplicate notifications

---

## API Endpoints

| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/api/v1/maintenance/categories/` | List all categories |
| GET | `/api/v1/maintenance/records/` | List maintenance records (filter by vehicle) |
| POST | `/api/v1/maintenance/records/` | Log a maintenance event |
| GET/PATCH/DELETE | `/api/v1/maintenance/records/{id}/` | Manage a record |
| GET | `/api/v1/maintenance/reminders/` | List reminders (filter by vehicle, status) |
| POST | `/api/v1/maintenance/reminders/` | Create a reminder |
| PATCH | `/api/v1/maintenance/reminders/{id}/` | Update reminder (e.g. snooze, dismiss) |

---

## Relationships

- **Vehicles** — each record/reminder belongs to a Vehicle
- **Notifications** — when a reminder is due, a Notification is created
- **AI Insights** — AI uses maintenance history to compute health scores and predictions

---

## Async Processing

A Celery task (`check_maintenance_reminders`) runs periodically (configurable via Django Celery Beat). It:

1. Queries all active reminders where `notification_sent = False`
2. Checks if `due_date <= today` OR `vehicle.current_odometer_km >= due_odometer_km`
3. Creates a Notification and sends a push notification via FCM
4. Sets `notification_sent = True`
