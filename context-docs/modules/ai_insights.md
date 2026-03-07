# Module: AI Insights

**Django App:** `apps.ai_insights`

---

## Purpose

The AI Insights module generates and stores AI-powered analysis of vehicle data. It provides predictive maintenance recommendations, fuel efficiency analysis, cost breakdowns, and an overall vehicle health score.

---

## Responsibilities

- Generating AI insights based on maintenance history and mileage data
- Computing vehicle health scores (0–100)
- Storing insights and scores with timestamps
- Allowing users to dismiss insights
- Providing prioritized insight lists (critical, high, medium, low)
- Exposing health score history for trend visualization

---

## Models

### `AIInsight`
A single AI-generated insight or recommendation.

Key fields:
- `vehicle`
- `insight_type` — maintenance_prediction | fuel_efficiency | cost_analysis | health_score | recommendation
- `priority` — low | medium | high | critical
- `title`, `summary`, `detail`
- `confidence_score` — 0.0 to 1.0
- `data_snapshot` — the input data snapshot used to generate the insight
- `is_dismissed`
- `valid_until` — expiry for time-sensitive insights

### `VehicleHealthScore`
A periodic health score snapshot.

Key fields:
- `score` — overall 0–100
- `maintenance_score`, `mileage_score`, `fuel_score` — sub-scores
- `computed_at`

---

## API Endpoints

| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/api/v1/ai-insights/` | List active insights (filter by vehicle) |
| POST | `/api/v1/ai-insights/{id}/dismiss/` | Dismiss an insight |
| GET | `/api/v1/ai-insights/health-scores/` | Get health score history |

---

## Relationships

- **Vehicles** — insights are computed per vehicle
- **Maintenance** — maintenance history is the primary input for predictions
- **Mileage** — fuel efficiency trends inform fuel and mileage insights

---

## AI Computation (Planned)

The AI computation pipeline is planned for premium users. It will:

1. Collect the last 12 months of maintenance records for the vehicle
2. Collect fuel refill and odometer history
3. Call an LLM (Claude API) or a rule-based engine to generate insights
4. Compute the health score from weighted sub-scores:
   - Maintenance: is the vehicle up-to-date on service?
   - Mileage: what is the current vs. expected odometer for the vehicle age?
   - Fuel: is fuel efficiency declining (sign of engine wear)?
5. Store the results as `AIInsight` and `VehicleHealthScore` records

See `planning/roadmap.md` for timeline.
