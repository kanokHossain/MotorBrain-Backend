# MotorBrain Backend

**Vehicle management platform — Django REST API + React Native Mobile App**

This is the main coordination repository for the MotorBrain project. It contains the Django backend API and the React Native mobile app as a Git submodule.

---

## Repository Structure

```
MotorBrain-Backend/
├── backend/                  # Django project
│   ├── manage.py
│   ├── motorbrain/           # Django core (settings, urls, celery)
│   │   └── settings/
│   │       ├── base.py
│   │       ├── development.py
│   │       └── production.py
│   └── apps/
│       ├── users/            # Authentication, profiles, subscriptions
│       ├── vehicles/         # Vehicle CRUD
│       ├── maintenance/      # Maintenance records and reminders
│       ├── mileage/          # Odometer, trips, fuel refills
│       ├── payments/         # Subscription payment history
│       ├── notifications/    # In-app + push notifications
│       └── ai_insights/      # AI-generated insights and health scores
├── mobile-app/               # React Native app (Git submodule)
├── context-docs/             # Permanent system knowledge
│   ├── README.md             # System entry point for developers and AI
│   ├── modules/              # Module documentation
│   ├── functional/           # Feature and workflow documentation
│   └── planning/             # Roadmap and ideas
├── docs/                     # Temporary implementation planning
├── requirements/
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

---

## Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL 16
- Redis 7
- Node.js 18+ (for mobile app)

### Clone with Submodule

```bash
git clone --recurse-submodules git@github-personal:kanokHossain/MotorBrain-Backend.git
cd MotorBrain-Backend
```

If already cloned without submodule:

```bash
git submodule update --init --recursive
```

### Backend Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements/development.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your local settings

# Run migrations
cd backend
python manage.py migrate

# Load initial maintenance categories
python manage.py loaddata apps/maintenance/fixtures/categories.json

# Start development server
python manage.py runserver
```

### Celery (for reminders and async tasks)

```bash
# In a separate terminal
celery -A motorbrain worker -l info

# Celery Beat (scheduled tasks)
celery -A motorbrain beat -l info
```

### Docker (full stack)

```bash
cp .env.example .env
docker-compose up
```

---

## API Documentation

Once the server is running:

| URL | Description |
|-----|-------------|
| `http://localhost:8000/api/docs/` | Swagger UI |
| `http://localhost:8000/api/redoc/` | ReDoc |
| `http://localhost:8000/api/schema/` | OpenAPI JSON schema |

---

## Context Documentation

For system architecture, module descriptions, and feature flows, see:

**[context-docs/README.md](context-docs/README.md)** — Start here.

This is the entry point for developers and AI agents to understand the system before implementing new features.

---

## Development Workflow

For every new feature:

1. **Update context** — `context-docs/modules/` and `context-docs/functional/`
2. **Create implementation plan** — `docs/` folder
3. **Implement** — write the code
4. **Clean up** — remove from `docs/`, update `context-docs/` if needed

---

## Mobile App

The React Native mobile app lives in `mobile-app/` as a Git submodule.

```bash
cd mobile-app
npm install
cd ios && bundle exec pod install && cd ..
npx react-native run-ios
```

See [mobile-app/README.md](mobile-app/README.md) for full mobile setup instructions.

---

## Repositories

| Repo | URL |
|------|-----|
| Backend (this repo) | `git@github-personal:kanokHossain/MotorBrain-Backend.git` |
| Mobile App | `git@github-personal:kanokHossain/MotorBrain-APP.git` |
