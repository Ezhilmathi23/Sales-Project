import pandas as pd
import numpy as np

pd.set_option("display.width", 120)

df = pd.read_csv("data/sales_data.csv", parse_dates=["date"])

print("=" * 60)
print("1. DATA OVERVIEW")
print("=" * 60)
print(df.info())
print("\nMissing values:\n", df.isna().sum())

# ---- Cleaning ----
# Fill missing discount_pct with 0 (assume no discount applied)
df["discount_pct"] = df["discount_pct"].fillna(0)

print("\n" + "=" * 60)
print("2. SUMMARY STATISTICS")
print("=" * 60)
print(df[["unit_price", "quantity", "revenue"]].describe().round(2))

# ---- GroupBy: revenue by category ----
print("\n" + "=" * 60)
print("3. REVENUE BY CATEGORY")
print("=" * 60)
by_category = (
    df.groupby("category")["revenue"]
    .agg(total_revenue="sum", avg_order_value="mean", orders="count")
    .sort_values("total_revenue", ascending=False)
    .round(2)
)
print(by_category)

# ---- GroupBy: revenue by region ----
print("\n" + "=" * 60)
print("4. REVENUE BY REGION")
print("=" * 60)
by_region = df.groupby("region")["revenue"].sum().sort_values(ascending=False).round(2)
print(by_region)

# ---- Pivot table: category x region ----
print("\n" + "=" * 60)
print("5. PIVOT TABLE: CATEGORY x REGION (total revenue)")
print("=" * 60)
pivot = pd.pivot_table(
    df, values="revenue", index="category", columns="region", aggfunc="sum"
).round(2)
print(pivot)

# ---- Monthly trend + rolling average ----
print("\n" + "=" * 60)
print("6. MONTHLY REVENUE TREND")
print("=" * 60)
monthly = df.set_index("date").resample("ME")["revenue"].sum().round(2)
print(monthly)

daily = df.set_index("date").resample("D")["revenue"].sum()
rolling_7d = daily.rolling(window=7).mean()

# ---- Top 10 highest-value orders ----
print("\n" + "=" * 60)
print("7. TOP 10 ORDERS BY REVENUE")
print("=" * 60)
print(df.nlargest(10, "revenue")[["order_id", "date", "category", "region", "revenue"]])

# ---- Save processed outputs for the visualization script ----
by_category.to_csv("data/by_category.csv")
by_region.to_csv("data/by_region.csv")
pivot.to_csv("data/pivot_category_region.csv")
monthly.to_csv("data/monthly_revenue.csv")
rolling_7d.to_csv("data/rolling_7d.csv")

print("\nProcessed summary files saved to data/")
