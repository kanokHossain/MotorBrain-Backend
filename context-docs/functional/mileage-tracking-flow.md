# Feature: Mileage & Fuel Tracking

## Related Modules
- [Vehicles](../modules/vehicles.md)
- [Mileage](../modules/mileage.md)
- [Maintenance](../modules/maintenance.md)

---

## Feature Description

Users can track their vehicle usage through odometer readings, individual trips, and fuel refill logs. The system calculates fuel efficiency (km/L) and cost-per-km after each full-tank fill, providing insight into vehicle running costs and efficiency trends.

---

## User Flow

### Logging an Odometer Reading

1. User taps "Log Odometer" in the vehicle's mileage section
2. User enters:
   - Odometer reading (km)
   - Timestamp (defaults to now)
   - Notes (optional)
3. App sends `POST /api/v1/mileage/odometer/`
4. Server saves and updates `vehicle.current_odometer_km` if value is higher

### Logging a Trip

1. User taps "Start Trip" or "Log Trip"
2. User enters:
   - Start odometer (km)
   - End odometer (optional, can be added later)
   - Start datetime
   - End datetime (optional)
   - Purpose (optional)
3. App sends `POST /api/v1/mileage/trips/`
4. `distance_km` is computed automatically as `end - start`

### Logging a Fuel Refill

1. User taps "Add Fuel" in the mileage section
2. User enters:
   - Date
   - Odometer reading
   - Liters filled
   - Cost per liter (optional)
   - Total cost (optional)
   - Full tank? (Yes/No)
   - Fuel station name (optional)
3. App sends `POST /api/v1/mileage/fuel/`
4. Server saves the refill
5. If `is_full_tank = True`, the Celery task `recalculate_fuel_efficiency` is triggered asynchronously
6. The task finds the previous full-tank fill and computes efficiency

### Viewing Fuel Efficiency

1. User opens the "Fuel & Mileage" stats screen for a vehicle
2. App fetches `GET /api/v1/mileage/fuel/?vehicle=<id>&ordering=-refill_date`
3. The most recent entries include pre-computed `fuel_efficiency_km_per_liter` and `cost_per_km`
4. App renders a chart showing efficiency trend over time

---

## Business Rules

- Odometer readings must be monotonically increasing (cannot log a reading lower than the current vehicle odometer)
- Fuel efficiency is only computed for full-tank fills (partial fills are tracked but not used in efficiency calculations)
- `total_cost = liters × cost_per_liter` if total_cost is not provided directly (computed in the app before submission)
- Mileage-based maintenance reminders are checked every time the vehicle odometer is updated

---

## System Behavior

- When a new odometer log, trip, or fuel refill is saved, if the new odometer value exceeds `vehicle.current_odometer_km`, the vehicle's odometer is updated
- This odometer update may trigger mileage-based maintenance reminder notifications
- Fuel efficiency calculation is asynchronous — it may appear after a short delay on the app

---

## Calculated Metrics

| Metric | Formula |
|--------|---------|
| Fuel Efficiency | `distance_since_last_full_fill ÷ liters` |
| Cost Per KM | `total_cost ÷ distance_since_last_full_fill` |
| Total Distance | `current_odometer - initial_odometer_at_registration` |
