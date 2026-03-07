# MotorBrain — System Context

## Product Vision

MotorBrain is a vehicle management platform that helps car and bike owners track their vehicle usage, maintenance history, and fuel consumption. The system provides intelligent reminders, AI-powered predictive maintenance insights, and a clean mobile-first experience.

The platform is designed to reduce unexpected vehicle breakdowns by keeping users informed about upcoming maintenance needs and by analyzing usage patterns to predict future service requirements.

---

## System Concept

Users register an account and add one or more vehicles. For each vehicle, they can:

- Log maintenance activities (oil changes, tyre replacements, battery, etc.)
- Log fuel refills and track fuel efficiency
- Record trips and odometer readings
- Receive proactive maintenance reminders based on time or mileage
- View AI-generated insights and vehicle health scores
- Manage subscription plans for premium features

---

## High-Level Architecture

```
Mobile App (React Native)
        |
        | REST API (HTTPS/JWT)
        |
Django Backend (DRF)
        |
   ┌────┴────┐
   |         |
PostgreSQL  Redis
(Database)  (Celery Broker / Cache)
        |
   Celery Workers
   (Async Tasks, Reminders)
        |
   Firebase Cloud Messaging
   (Push Notifications)
```

### Repositories

| Repo | Purpose |
|------|---------|
| `MotorBrain-Backend` | Django API, main coordination repo, contains mobile app as submodule |
| `MotorBrain-APP` | React Native mobile application (submodule at `mobile-app/`) |

---

## System Modules

The system is divided into the following modules. Each module is a Django app.

| Module | Django App | Description |
|--------|-----------|-------------|
| [Users](modules/users.md) | `apps.users` | Authentication, profiles, subscriptions |
| [Vehicles](modules/vehicles.md) | `apps.vehicles` | Vehicle CRUD and ownership |
| [Maintenance](modules/maintenance.md) | `apps.maintenance` | Maintenance records and reminders |
| [Mileage](modules/mileage.md) | `apps.mileage` | Odometer logs, trips, fuel refills |
| [Payments](modules/payments.md) | `apps.payments` | Subscription payment tracking |
| [Notifications](modules/notifications.md) | `apps.notifications` | In-app and push notifications |
| [AI Insights](modules/ai_insights.md) | `apps.ai_insights` | Predictive maintenance, health scores |

---

## Functional Features

| Feature | Document |
|---------|---------|
| User Authentication Flow | [functional/user-authentication-flow.md](functional/user-authentication-flow.md) |
| Vehicle Maintenance Logging | [functional/vehicle-maintenance-flow.md](functional/vehicle-maintenance-flow.md) |
| Mileage & Fuel Tracking | [functional/mileage-tracking-flow.md](functional/mileage-tracking-flow.md) |
| Subscription Management | [functional/subscription-management.md](functional/subscription-management.md) |
| Maintenance Reminders | [functional/maintenance-reminders.md](functional/maintenance-reminders.md) |
| AI Predictive Insights | [functional/ai-insights-flow.md](functional/ai-insights-flow.md) |

---

## Technology Stack

**Backend**
- Python 3.12+
- Django 6.x
- Django REST Framework 3.x
- JWT Authentication (djangorestframework-simplejwt)
- PostgreSQL 16
- Celery + Redis (async tasks and beat scheduling)
- Firebase Admin SDK (push notifications)
- DRF Spectacular (OpenAPI/Swagger docs)

**Mobile**
- React Native 0.84+
- TypeScript
- React Navigation
- Redux Toolkit
- Axios
- React Native Firebase (FCM)

---

## Development Workflow

For every new feature, follow this process:

1. **Update Context** — update `context-docs/modules/` and `context-docs/functional/`
2. **Create Implementation Plan** — create a doc in `docs/`
3. **Implement** — write the code
4. **Clean Up** — remove the `docs/` implementation plan; update `context-docs/` if behavior changed

See [planning/roadmap.md](planning/roadmap.md) for the product roadmap.

---

## Repository Structure

```
MotorBrain-Backend/
├── backend/                  # Django project
│   ├── motorbrain/           # Django settings, urls, celery
│   └── apps/
│       ├── users/
│       ├── vehicles/
│       ├── maintenance/
│       ├── mileage/
│       ├── payments/
│       ├── notifications/
│       └── ai_insights/
├── mobile-app/               # React Native app (Git submodule)
├── context-docs/             # Permanent system knowledge (this folder)
│   ├── README.md             # This file — system entry point
│   ├── modules/              # Module documentation
│   ├── functional/           # Feature and workflow documentation
│   └── planning/             # Roadmap and future ideas
├── docs/                     # Temporary implementation planning
├── requirements/
├── Dockerfile
├── docker-compose.yml
└── README.md
```
