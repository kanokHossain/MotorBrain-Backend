# Module: Notifications

**Django App:** `apps.notifications`

---

## Purpose

The Notifications module manages in-app notifications and coordinates push notification delivery via Firebase Cloud Messaging (FCM).

---

## Responsibilities

- Storing in-app notification records per user
- Tracking read/unread status
- Tracking push notification delivery status
- Providing notification list and mark-as-read API endpoints
- Sending push notifications via FCM (through a service helper)

---

## Models

### `Notification`
An in-app notification record.

Key fields:
- `user` — recipient
- `notification_type` — maintenance_reminder | mileage_threshold | subscription | ai_insight | system
- `title`, `body`
- `data` — JSON payload for mobile deep linking (e.g. `{"reminder_id": 5, "vehicle_id": 2}`)
- `is_read` — read/unread flag
- `push_sent` — whether FCM push was dispatched
- `vehicle` — optional reference to the related vehicle

---

## API Endpoints

| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/api/v1/notifications/` | List notifications (`?unread=true` filter) |
| POST | `/api/v1/notifications/mark-all-read/` | Mark all as read |
| GET/PATCH | `/api/v1/notifications/{id}/` | Get or update a notification |

---

## Relationships

- **Users** — each Notification belongs to a User
- **Vehicles** — optional vehicle reference for context
- **Maintenance** — maintenance reminders create Notifications
- **AI Insights** — new AI insights may create Notifications

---

## Push Notification Flow

1. A Celery task (e.g. `check_maintenance_reminders`) detects a due event
2. It creates a `Notification` DB record
3. It calls the FCM service with the user's `fcm_token`, `title`, and `body`
4. On success, `push_sent = True` and `push_sent_at` is recorded
5. The mobile app displays the notification in the notification center
