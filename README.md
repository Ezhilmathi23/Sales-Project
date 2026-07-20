# Retail Sales Analysis Project

A hands-on project using **NumPy**, **Pandas**, and **Matplotlib** to generate,
clean, analyze, and visualize a synthetic retail sales dataset.

## Structure

```
sales_project/
├── generate_data.py   # NumPy: builds a synthetic 1-year sales dataset
├── analysis.py        # Pandas: cleaning, groupby, pivot tables, resampling
├── visualize.py       # Matplotlib: 5 charts from the analysis output
├── data/
│   ├── sales_data.csv            # raw generated dataset (~10k orders)
│   └── ...                       # processed summary CSVs
└── charts/
    ├── 01_revenue_by_category.png
    ├── 02_revenue_by_region.png
    ├── 03_monthly_trend.png
    ├── 04_rolling_average.png
    └── 05_heatmap_category_region.png
```

## How to run

```bash
pip install numpy pandas matplotlib
python generate_data.py   # creates data/sales_data.csv
python analysis.py        # prints analysis, saves summary CSVs
python visualize.py       # saves 5 PNG charts to charts/
```

## What each script demonstrates

**generate_data.py (NumPy)**
- `np.random.poisson`, `np.random.choice`, `np.random.uniform` for realistic
  synthetic data with weekend/seasonal patterns
- Vectorized calculations for revenue and discounts

**analysis.py (Pandas)**
- Reading CSVs with `parse_dates`, checking `.info()` / `.isna()`
- Cleaning: `fillna()`
- `.describe()` for summary statistics
- `.groupby().agg()` for category/region breakdowns
- `pd.pivot_table()` for a category × region matrix
- `.resample("ME")` for monthly aggregation and `.rolling()` for a 7-day
  moving average
- `.nlargest()` to find top orders

**visualize.py (Matplotlib)**
- Horizontal bar chart, pie chart, line chart, rolling-average line chart,
  and a manually built heatmap with annotated cells
- Custom axis formatting (`FuncFormatter` for currency), styling, and
  `tight_layout()`

## Ideas to extend this yourself

- Swap in a real dataset (e.g. Kaggle retail data) and rerun the same pipeline
- Add a `customer_id` column and compute repeat-purchase rate
- Try `df.corr()` and a scatter plot between discount % and quantity
- Build a simple linear regression (NumPy `polyfit`) to forecast next month's revenue
