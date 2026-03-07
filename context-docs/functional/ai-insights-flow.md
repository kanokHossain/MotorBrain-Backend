# Feature: AI Predictive Insights

## Related Modules
- [AI Insights](../modules/ai_insights.md)
- [Vehicles](../modules/vehicles.md)
- [Maintenance](../modules/maintenance.md)
- [Mileage](../modules/mileage.md)
- [Notifications](../modules/notifications.md)

---

## Feature Description

MotorBrain uses AI to analyze vehicle data and generate actionable maintenance predictions, fuel efficiency insights, and an overall vehicle health score. AI features are available to Basic and Premium subscribers.

---

## User Flow

### Viewing AI Insights

1. User opens the "AI Insights" section for a vehicle
2. App fetches `GET /api/v1/ai-insights/?vehicle=<id>`
3. Insights are displayed grouped by priority (Critical → High → Medium → Low)
4. Each insight shows:
   - Title and summary
   - Priority badge
   - Insight type icon
5. User taps an insight for full detail
6. User can dismiss an insight they've acted on

### Viewing Health Score

1. User opens vehicle dashboard
2. A health score gauge (0–100) is displayed prominently
3. Tapping shows sub-scores: Maintenance, Mileage, Fuel
4. A history chart shows score trend over the last 10 computations

### Dismissing an Insight

1. User swipes left on an insight or taps "Dismiss"
2. App sends `POST /api/v1/ai-insights/{id}/dismiss/`
3. Insight is hidden from the active list

---

## Insight Types

| Type | Description |
|------|-------------|
| `maintenance_prediction` | "Based on your mileage rate, your engine oil will be due in ~15 days" |
| `fuel_efficiency` | "Your fuel efficiency dropped 12% over the last 3 fills — possible air filter issue" |
| `cost_analysis` | "You've spent $320 on maintenance this year — 40% above average for this vehicle age" |
| `health_score` | Overall health score summary |
| `recommendation` | General recommendations based on vehicle age, type, and usage |

---

## Business Rules

- AI features are only available to Basic and Premium subscribers
- Insights have a `valid_until` timestamp — expired insights are not shown
- Health scores are computed periodically (weekly for Basic, daily for Premium)
- The minimum data required to generate insights: at least 2 maintenance records OR 3 fuel refills

---

## System Behavior

### AI Computation Pipeline (Planned)

1. Celery task collects vehicle data snapshot:
   - Last 12 months of maintenance records
   - Last 20 fuel refills with efficiency values
   - Current odometer vs. vehicle age
2. Data is passed to the AI engine (Claude API or rule-based engine)
3. Insights are generated with confidence scores
4. Health sub-scores are computed:
   - **Maintenance score**: overdue items reduce score; recent service improves it
   - **Mileage score**: compares actual km/year vs. expected for vehicle type
   - **Fuel score**: efficiency trend (declining = lower score)
5. Results are stored as `AIInsight` and `VehicleHealthScore` records
6. If a critical insight is generated, a push notification is sent

### Current State

The AI computation pipeline is **planned** for v2. In v1, a rule-based heuristic engine provides basic insights. Full LLM integration is on the roadmap.
