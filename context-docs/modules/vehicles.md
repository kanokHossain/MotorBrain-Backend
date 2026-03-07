# Module: Vehicles

**Django App:** `apps.vehicles`

---

## Purpose

The Vehicles module manages the fleet of cars and bikes that a user owns. All other feature modules (maintenance, mileage, AI insights) are scoped to a specific vehicle.

---

## Responsibilities

- CRUD operations for user vehicles
- Storing vehicle metadata (make, model, year, type, fuel type)
- Tracking the current odometer reading
- Soft-delete via `is_active` flag (vehicles are never hard-deleted)
- Image upload for vehicle photos

---

## Models

### `Vehicle`
The primary model. Belongs to a `User` via `owner` FK.

Key fields:
- `name` — user-defined label (e.g. "My Honda")
- `make`, `model`, `year`
- `vehicle_type` — car, bike, truck, other
- `fuel_type` — petrol, diesel, electric, hybrid, CNG, LPG
- `license_plate`, `vin`
- `current_odometer_km` — updated automatically when mileage or maintenance is logged
- `is_active` — soft delete flag

---

## API Endpoints

| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/api/v1/vehicles/` | List user's vehicles |
| POST | `/api/v1/vehicles/` | Add a new vehicle |
| GET | `/api/v1/vehicles/{id}/` | Get vehicle detail |
| PATCH | `/api/v1/vehicles/{id}/` | Update vehicle |
| DELETE | `/api/v1/vehicles/{id}/` | Soft-delete vehicle |

---

## Relationships

- **Users** — each Vehicle belongs to one User
- **Maintenance** — a Vehicle has many MaintenanceRecords and MaintenanceReminders
- **Mileage** — a Vehicle has many OdometerLogs, Trips, FuelRefills
- **Notifications** — Notifications can reference a Vehicle
- **AI Insights** — AIInsights and VehicleHealthScores belong to a Vehicle

---

## Business Rules

- A user can own multiple vehicles (Free plan: max 2 vehicles; Premium: unlimited)
- Deleting a vehicle is a soft-delete — data is retained
- The `current_odometer_km` field is updated whenever a new mileage log or maintenance record is saved with a higher odometer value
