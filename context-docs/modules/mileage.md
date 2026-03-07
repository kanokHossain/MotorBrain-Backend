# Module: Mileage

**Django App:** `apps.mileage`

---

## Purpose

The Mileage module tracks vehicle usage through odometer readings, trips, and fuel refills. It calculates fuel efficiency and cost-per-km metrics, and feeds odometer data into the maintenance reminder system.

---

## Responsibilities

- Logging odometer readings over time
- Recording trips with start/end odometer values
- Logging fuel refills with liters, cost, and station info
- Calculating fuel efficiency (km/L) after each full-tank fill
- Calculating cost-per-km
- Updating the vehicle's `current_odometer_km` on new log entries
- Triggering mileage-based maintenance reminders

---

## Models

### `OdometerLog`
A timestamped odometer reading. Used to track cumulative distance without requiring a trip structure.

### `Trip`
A point-to-point journey with start/end odometer. `distance_km` is a computed property.

### `FuelRefill`
A fuel refill entry. After a full-tank fill is logged, the Celery task `recalculate_fuel_efficiency` computes:
- `fuel_efficiency_km_per_liter` — distance since last full fill ÷ liters
- `cost_per_km` — total_cost ÷ distance

---

## API Endpoints

| Method | Endpoint | Description |
|--------|---------|-------------|
| GET/POST | `/api/v1/mileage/odometer/` | List or create odometer logs |
| GET/POST | `/api/v1/mileage/trips/` | List or create trips |
| GET/POST | `/api/v1/mileage/fuel/` | List or create fuel refills |

All endpoints support `?vehicle=<id>` query param to filter by vehicle.

---

## Relationships

- **Vehicles** — all mileage data belongs to a Vehicle
- **Maintenance** — mileage data drives mileage-based reminders
- **AI Insights** — fuel efficiency trends feed into AI analysis

---

## Fuel Efficiency Calculation

Triggered asynchronously via Celery after each new `FuelRefill` is saved:

1. Find the previous full-tank fill for the same vehicle
2. Compute `distance = current_odometer - prev_odometer`
3. `km_per_liter = distance / liters`
4. `cost_per_km = total_cost / distance`
5. Save results to the refill record
