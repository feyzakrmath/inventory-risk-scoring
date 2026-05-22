
Explainable inventory waste risk scoring model using sales velocity and expiry analysis

# Inventory Risk Scoring

This project implements an explainable inventory waste risk scoring framework designed to identify inventory lots that are at risk of expiring before being sold.

## Objective

The goal is to create an interpretable mathematical risk score based on:

- inventory quantity
- remaining shelf life
- historical sales velocity

This project intentionally avoids machine learning approaches and focuses on transparency and operational interpretability.

---

## Project Structure

| File | Description |
|---|---|
| risk_scoring_model.ipynb | Jupyter notebook analysis |
| risk_model.py | End-to-end Python scoring pipeline |
| risk_score_explanation.md | Mathematical and business explanation |
| top_20_risky_inventory.csv | Highest-risk inventory records |

---

## Risk Score Logic

Main risk formulation:

```python
core_risk = coverage_days / (days_to_expiry + 1)
```

Final score:

```python
risk_score =
0.8 * core_risk
+ 0.2 * stock_norm
```

---

## Features Used

- on_hand_qty
- daily_velocity
- coverage_days
- days_to_expiry

---

## Risk Levels

| Score Range | Label |
|---|---|
| < 0.5 | Low |
| 0.5 - 1 | Medium |
| >= 1 | High |

---

