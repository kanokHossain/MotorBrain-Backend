# Module: Users

**Django App:** `apps.users`

---

## Purpose

The Users module handles all user identity, authentication, and account management. It is the foundation of the entire platform — all other modules require a user context.

---

## Responsibilities

- User registration and email-based authentication
- JWT token issuance, refresh, and blacklisting (logout)
- User profile management (name, phone, avatar)
- Password change
- Email verification status tracking
- FCM (Firebase Cloud Messaging) token management for push notifications
- Subscription plan tracking (Free, Basic, Premium)

---

## Models

### `User`
Custom user model extending `AbstractBaseUser`. Uses email as the primary identifier (not username).

Key fields:
- `email` — unique identifier
- `first_name`, `last_name`, `phone_number`
- `avatar` — profile picture
- `is_verified` — email verification flag
- `fcm_token` — Firebase token for push notifications

### `UserSubscription`
One-to-one relation with User. Tracks the active subscription plan.

Plans: `free`, `basic`, `premium`
Statuses: `active`, `expired`, `cancelled`, `trial`

---

## API Endpoints

| Method | Endpoint | Description |
|--------|---------|-------------|
| POST | `/api/v1/auth/register/` | Create new account |
| POST | `/api/v1/auth/login/` | Obtain JWT token pair |
| POST | `/api/v1/auth/token/refresh/` | Refresh access token |
| POST | `/api/v1/auth/logout/` | Blacklist refresh token |
| GET/PATCH | `/api/v1/auth/profile/` | Get or update profile |
| POST | `/api/v1/auth/profile/fcm-token/` | Update push notification token |
| POST | `/api/v1/auth/profile/change-password/` | Change password |

---

## Relationships

- **Vehicles** — a User owns many Vehicles
- **Payments** — a User has many Payments
- **Notifications** — a User receives many Notifications
- **UserSubscription** — a User has one Subscription

---

## Authentication Flow

1. User registers via `/register/`
2. A `UserSubscription` (Free plan) is automatically created
3. User logs in via `/login/` and receives access + refresh JWT tokens
4. Mobile app includes the access token in `Authorization: Bearer <token>` header
5. On token expiry, app refreshes via `/token/refresh/`
6. On logout, the refresh token is blacklisted

---

## Premium Feature Gating

The `UserSubscription.is_premium` property returns `True` if the user has an active Basic or Premium plan. API views and mobile screens use this to gate premium features.
