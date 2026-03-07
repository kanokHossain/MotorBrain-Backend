# Module: Payments

**Django App:** `apps.payments`

---

## Purpose

The Payments module records subscription payment transactions and integrates with payment providers (Stripe, bKash, etc.) to unlock premium features.

---

## Responsibilities

- Storing payment transaction records
- Linking payments to user subscriptions
- Supporting multiple currencies and payment providers
- Providing payment history to users

---

## Models

### `Payment`
A single payment transaction.

Key fields:
- `user` — the paying user
- `amount`, `currency`
- `status` — pending | completed | failed | refunded
- `plan` — which subscription plan was purchased
- `payment_provider` — e.g. Stripe, bKash
- `transaction_id` — external provider reference

---

## API Endpoints

| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/api/v1/payments/` | List user's payment history |

---

## Relationships

- **Users** — each Payment belongs to a User
- **UserSubscription** — after a successful payment, the UserSubscription is updated

---

## Notes

Payment provider webhook integration (Stripe webhooks, etc.) is not yet implemented. This is planned in the product roadmap. The current implementation supports recording payments after the fact.
