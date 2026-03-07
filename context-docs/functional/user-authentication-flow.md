# Feature: User Authentication Flow

## Related Modules
- [Users](../modules/users.md)

---

## Feature Description

All users must register and authenticate before accessing the application. The system uses JWT (JSON Web Tokens) for stateless authentication. The mobile app stores tokens securely and handles automatic refresh.

---

## User Flow

### Registration

1. User opens the app and taps "Sign Up"
2. User enters: email, first name, last name, password, confirm password
3. App sends `POST /api/v1/auth/register/`
4. Server creates the user account and a Free subscription
5. Server returns user data
6. App redirects to the login screen (or auto-login)

### Login

1. User enters email and password
2. App sends `POST /api/v1/auth/login/`
3. Server returns `access` token (short-lived) and `refresh` token (long-lived)
4. App stores both tokens securely (Keychain on iOS, Keystore on Android)
5. App includes `Authorization: Bearer <access_token>` in all subsequent requests

### Token Refresh

1. When an API request returns `401 Unauthorized`
2. App sends `POST /api/v1/auth/token/refresh/` with the stored refresh token
3. Server returns a new access token (and rotates the refresh token)
4. App retries the original request with the new token

### Logout

1. User taps "Logout"
2. App sends `POST /api/v1/auth/logout/` with the refresh token
3. Server blacklists the refresh token (it cannot be used again)
4. App clears stored tokens and redirects to login

---

## Business Rules

- Passwords must meet Django's default password validators (min length 8, not entirely numeric, etc.)
- Email addresses must be unique across the system
- JWT access tokens expire in 60 minutes (configurable)
- JWT refresh tokens expire in 7 days (configurable)
- Refresh token rotation is enabled — each refresh issues a new refresh token
- Blacklisted refresh tokens cannot be used for further refresh attempts

---

## System Behavior

- A new `UserSubscription` with `plan=free` is automatically created on registration
- The FCM token is not set at registration — it is updated after the mobile app receives the Firebase device token
- Failed login attempts are not rate-limited in the initial version (planned for v2)

---

## API Reference

| Method | Endpoint | Auth |
|--------|---------|------|
| POST | `/api/v1/auth/register/` | Public |
| POST | `/api/v1/auth/login/` | Public |
| POST | `/api/v1/auth/token/refresh/` | Public (refresh token) |
| POST | `/api/v1/auth/logout/` | Authenticated |
| GET/PATCH | `/api/v1/auth/profile/` | Authenticated |
