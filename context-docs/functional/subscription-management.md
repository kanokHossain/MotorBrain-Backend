# Feature: Subscription Management

## Related Modules
- [Users](../modules/users.md)
- [Payments](../modules/payments.md)
- [Notifications](../modules/notifications.md)

---

## Feature Description

MotorBrain offers a tiered subscription model. The Free plan provides core features. Basic and Premium plans unlock advanced features including unlimited vehicles, AI insights, and extended history.

---

## Subscription Plans

| Feature | Free | Basic | Premium |
|---------|------|-------|---------|
| Vehicles | Up to 2 | Up to 5 | Unlimited |
| Maintenance records | 10/vehicle | 50/vehicle | Unlimited |
| Fuel logs | 20/vehicle | Unlimited | Unlimited |
| Maintenance reminders | 2/vehicle | 5/vehicle | Unlimited |
| AI Insights | — | Basic | Full (predictive) |
| Vehicle Health Score | — | Yes | Yes |
| Receipt photos | — | Yes | Yes |
| Priority support | — | — | Yes |

---

## User Flow

### Upgrading Subscription

1. User taps "Go Premium" or sees a paywall for a premium feature
2. App shows the subscription plans screen
3. User selects a plan (Basic or Premium)
4. User completes payment via integrated provider (Stripe / bKash)
5. On successful payment:
   - A `Payment` record is created with `status=completed`
   - The `UserSubscription` plan and status are updated
   - A confirmation notification is sent
6. Premium features are immediately unlocked

### Subscription Expiry

1. Celery beat checks for expired subscriptions daily
2. When `expires_at < now` and `status=active`:
   - Status is set to `expired`
   - User receives a renewal reminder notification
3. User can renew from the app's subscription screen

---

## Business Rules

- Each user has exactly one `UserSubscription` (created on registration)
- A new user starts on the Free plan with no expiry
- Paid plans have an `expires_at` date set based on billing cycle (monthly/yearly)
- The `is_premium` property on `UserSubscription` governs all feature gating checks
- Downgrading is allowed — existing data is never deleted on downgrade

---

## System Behavior

- API views check `request.user.subscription.is_premium` for gated endpoints
- Exceeding plan limits returns HTTP 402 Payment Required with a clear message
- Payment provider webhooks update the subscription status on payment events
