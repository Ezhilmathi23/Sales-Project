import numpy as np
import pandas as pd

np.random.seed(42)

# ---- Config ----
N_DAYS = 365
START_DATE = "2025-01-01"

CATEGORIES = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books"]
REGIONS = ["North", "South", "East", "West"]

# Base price ranges per category (min, max)
PRICE_RANGES = {
    "Electronics": (50, 800),
    "Clothing": (15, 120),
    "Home & Garden": (10, 300),
    "Sports": (20, 250),
    "Books": (8, 40),
}

# ---- Build date range ----
dates = pd.date_range(start=START_DATE, periods=N_DAYS, freq="D")

rows = []
for date in dates:
    # More transactions on weekends, seasonal bump in Nov/Dec
    is_weekend = date.dayofweek >= 5
    month = date.month
    seasonal_boost = 1.6 if month in (11, 12) else 1.0
    base_transactions = np.random.poisson(lam=25 * (1.3 if is_weekend else 1.0) * seasonal_boost)

    for _ in range(base_transactions):
        category = np.random.choice(CATEGORIES, p=[0.25, 0.25, 0.2, 0.15, 0.15])
        region = np.random.choice(REGIONS)
        low, high = PRICE_RANGES[category]
        unit_price = np.round(np.random.uniform(low, high), 2)
        quantity = np.random.randint(1, 6)
        # Random discount, more common in Nov/Dec sales
        discount_pct = np.random.choice(
            [0, 0.05, 0.10, 0.20, 0.30],
            p=[0.5, 0.2, 0.15, 0.1, 0.05] if month not in (11, 12) else [0.2, 0.2, 0.25, 0.2, 0.15],
        )
        revenue = np.round(unit_price * quantity * (1 - discount_pct), 2)

        rows.append({
            "date": date,
            "category": category,
            "region": region,
            "unit_price": unit_price,
            "quantity": quantity,
            "discount_pct": discount_pct,
            "revenue": revenue,
        })

df = pd.DataFrame(rows)
df["order_id"] = np.arange(1, len(df) + 1)
df = df[["order_id", "date", "category", "region", "unit_price", "quantity", "discount_pct", "revenue"]]

# Introduce a few missing values on purpose, to practice cleaning
missing_idx = np.random.choice(df.index, size=15, replace=False)
df.loc[missing_idx, "discount_pct"] = np.nan

out_path = "data/sales_data.csv"
df.to_csv(out_path, index=False)

print(f"Generated {len(df):,} rows -> {out_path}")
print(df.head())
