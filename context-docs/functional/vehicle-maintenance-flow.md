# Feature: Vehicle Maintenance Logging

## Related Modules
- [Vehicles](../modules/vehicles.md)
- [Maintenance](../modules/maintenance.md)
- [Notifications](../modules/notifications.md)
- [AI Insights](../modules/ai_insights.md)

---

## Feature Description

Users can log all maintenance activities performed on their vehicles. Each log entry represents a single service event. The complete history is stored and can be reviewed chronologically. The system uses this data to suggest reminders and generate AI insights.

---

## User Flow

### Logging Maintenance

1. User selects a vehicle from the dashboard
2. User taps "Add Maintenance" or "Log Service"
3. User fills in:
   - Category (from predefined list: Engine Oil, Tyres, Battery, etc.)
   - Part Name
   - Brand (optional)
   - Cost (optional)
   - Service Date
   - Odometer reading at service time
   - Notes (optional)
   - Receipt photo (optional)
4. App sends `POST /api/v1/maintenance/records/`
5. Server saves the record
6. Server updates `vehicle.current_odometer_km` if the new reading is higher
7. App shows confirmation and returns to maintenance history

### Viewing Maintenance History

1. User taps "Maintenance" tab for a vehicle
2. App fetches `GET /api/v1/maintenance/records/?vehicle=<id>`
3. Records are displayed chronologically (newest first)
4. User can tap a record to view full details or edit/delete it

### Setting a Reminder

1. After logging maintenance (or separately), user taps "Set Reminder"
2. User configures:
   - Reminder name (e.g. "Next Oil Change")
   - Trigger type: Time, Mileage, or Both
   - If Time: interval in days (e.g. 90 days → system computes due_date)
   - If Mileage: interval in km (e.g. 5000 km → system computes due_odometer_km)
3. App sends `POST /api/v1/maintenance/reminders/`
4. Server creates the reminder in `active` status

---

## Business Rules

- Odometer reading at service must be >= vehicle's current recorded odometer
- Cost is optional but helps with cost analysis features
- Receipt image is limited to 5MB (handled in the API)
- A reminder due_date is computed as: `service_date + interval_days`
- A reminder due_odometer is computed as: `odometer_at_service + interval_km`
- A reminder stays in `active` status until the user completes, dismisses, or snoozes it
- Free plan: up to 10 maintenance records per vehicle
- Premium plan: unlimited records

---

## System Behavior

- When a new maintenance record is saved, the server checks if any existing reminders for that category on that vehicle should be marked `completed`
- The Celery beat task `check_maintenance_reminders` runs daily to find due reminders and send push notifications
- Each reminder is only notified once (`notification_sent=True` after first push)
- Users can snooze a reminder (sets `snoozed_until` date and resets notification flag)

---

## Maintenance Categories (Predefined)

- Engine Oil
- Gearbox / Transmission Oil
- Brake Pads / Brake Shoes
- Tyres
- Battery
- Air Filter
- Fuel Filter
- Spark Plugs
- Coolant
- Brake Fluid
- Chain Lubrication (bikes)
- Drive Belt
- Windshield Wipers
- Other
