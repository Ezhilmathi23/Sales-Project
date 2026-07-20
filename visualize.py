"""
03_visualize.py
Matplotlib charts built from the summary CSVs produced by 02_analysis.py.
Run after 02_analysis.py. Saves PNGs to charts/.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

plt.style.use("seaborn-v0_8-whitegrid")

# ---- Load processed data ----
by_category = pd.read_csv("data/by_category.csv", index_col="category")
by_region = pd.read_csv("data/by_region.csv", index_col="region")["revenue"]
pivot = pd.read_csv("data/pivot_category_region.csv", index_col="category")
monthly = pd.read_csv("data/monthly_revenue.csv", index_col="date", parse_dates=True)["revenue"]
rolling_7d = pd.read_csv("data/rolling_7d.csv", index_col="date", parse_dates=True)["revenue"]

money_fmt = mticker.FuncFormatter(lambda x, _: f"${x:,.0f}")

# ---- Chart 1: Bar chart — revenue by category ----
fig, ax = plt.subplots(figsize=(8, 5))
by_category["total_revenue"].sort_values().plot(kind="barh", color="#4C72B0", ax=ax)
ax.set_title("Total Revenue by Category", fontsize=14, fontweight="bold")
ax.set_xlabel("Revenue")
ax.xaxis.set_major_formatter(money_fmt)
plt.tight_layout()
plt.savefig("charts/01_revenue_by_category.png", dpi=150)
plt.close()

# ---- Chart 2: Pie chart — revenue share by region ----
fig, ax = plt.subplots(figsize=(6, 6))
ax.pie(by_region, labels=by_region.index, autopct="%1.1f%%", startangle=90,
       colors=["#4C72B0", "#DD8452", "#55A868", "#C44E52"])
ax.set_title("Revenue Share by Region", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("charts/02_revenue_by_region.png", dpi=150)
plt.close()

# ---- Chart 3: Line chart — monthly revenue trend ----
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(monthly.index, monthly.values, marker="o", color="#4C72B0", linewidth=2)
ax.set_title("Monthly Revenue Trend (2025)", fontsize=14, fontweight="bold")
ax.set_ylabel("Revenue")
ax.yaxis.set_major_formatter(money_fmt)
ax.set_xlabel("Month")
fig.autofmt_xdate()
plt.tight_layout()
plt.savefig("charts/03_monthly_trend.png", dpi=150)
plt.close()

# ---- Chart 4: Line chart — daily revenue with 7-day rolling average ----
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(rolling_7d.index, rolling_7d.values, color="#C44E52", linewidth=2, label="7-day rolling avg")
ax.set_title("Daily Revenue — 7-Day Rolling Average", fontsize=14, fontweight="bold")
ax.set_ylabel("Revenue")
ax.yaxis.set_major_formatter(money_fmt)
ax.legend()
plt.tight_layout()
plt.savefig("charts/04_rolling_average.png", dpi=150)
plt.close()

# ---- Chart 5: Heatmap-style — category x region ----
fig, ax = plt.subplots(figsize=(8, 5))
im = ax.imshow(pivot.values, cmap="Blues", aspect="auto")
ax.set_xticks(range(len(pivot.columns)))
ax.set_xticklabels(pivot.columns)
ax.set_yticks(range(len(pivot.index)))
ax.set_yticklabels(pivot.index)
ax.set_title("Revenue Heatmap: Category x Region", fontsize=14, fontweight="bold")
for i in range(len(pivot.index)):
    for j in range(len(pivot.columns)):
        ax.text(j, i, f"${pivot.values[i, j]/1000:.0f}k", ha="center", va="center",
                color="white" if pivot.values[i, j] > pivot.values.max() * 0.5 else "black", fontsize=9)
fig.colorbar(im, ax=ax, label="Revenue ($)")
plt.tight_layout()
plt.savefig("charts/05_heatmap_category_region.png", dpi=150)
plt.close()

print("Saved 5 charts to charts/")
