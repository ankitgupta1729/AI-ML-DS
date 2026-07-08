# demo.db Contents

## Tables

- `spending_events`
- `electricity_plans`

## Schema

```sql
CREATE TABLE spending_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    plan_name TEXT NOT NULL,
    billing_start DATE NOT NULL,
    billing_end DATE NOT NULL,
    amount_due REAL
);

CREATE TABLE electricity_plans (
    plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_name TEXT NOT NULL,
    plan_description TEXT NOT NULL,
    selling_points TEXT NOT NULL
);
```

## spending_events

| event_id | customer_id | plan_name | billing_start | billing_end | amount_due |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | Standard Plan | 2024-01-01 | 2024-01-31 | 50.0 |
| 2 | 1 | Standard Plan | 2024-02-01 | 2024-02-29 | 55.0 |
| 3 | 1 | Standard Plan | 2024-03-01 | 2024-03-31 | 53.0 |
| 4 | 1 | Standard Plan | 2024-04-01 | 2024-04-30 | 52.0 |
| 5 | 1 | Standard Plan | 2024-05-01 | 2024-05-31 | 54.0 |
| 6 | 1 | Standard Plan | 2024-06-01 | 2024-06-30 | 56.0 |
| 7 | 1 | Eco Plan | 2024-07-01 | 2024-07-31 | 58.0 |
| 8 | 1 | Eco Plan | 2024-08-01 | 2024-08-31 | 57.0 |
| 9 | 1 | Eco Plan | 2024-09-01 | 2024-09-30 | 59.0 |
| 10 | 1 | Standard Plan | 2024-10-01 | 2024-10-31 | 60.0 |
| 11 | 1 | Standard Plan | 2024-11-01 | 2024-11-30 | 62.0 |
| 12 | 1 | Standard Plan | 2024-12-01 | 2024-12-31 | 63.0 |

## electricity_plans

| plan_id | plan_name | plan_description | selling_points |
| --- | --- | --- | --- |
| 1 | Standard Plan | A well-rounded electricity plan designed for typical households, offering stable pricing and reliable service without any peak-hour surcharges. | Affordable rates, predictable billing, ideal for families |
| 2 | Eco Plan | A renewable energy plan that prioritizes sustainability by sourcing electricity from solar, wind, and hydroelectric power. Perfect for environmentally conscious consumers. | 100% green energy, reduces carbon footprint, government incentives may apply |
| 3 | Night Plan | An electricity plan that provides significant cost savings for customers who consume most of their energy during off-peak nighttime hours. Ideal for night-shift workers and EV owners. | Lower rates at night, great for electric vehicle charging, smart meter integration |
