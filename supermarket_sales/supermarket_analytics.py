# -*- coding: utf-8 -*-
"""
supermarket_analytics.py
========================
Supermarket Sales Analysis - full pipeline
  1. Load & inspect dataset
  2. Data quality checks (missing / incorrect values)
  3. Feature engineering  (Sales = Quantity x Unit Price)
  4. Group & summarise    (totals, counts, averages)
  5. Visualisations       (bar, pie, line, heatmap, box)
  6. Business insights    (printed report)

Dependencies:
    pip install pandas matplotlib seaborn
"""

import os
import sys
import warnings
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# Force UTF-8 output so Unicode chars print safely on all terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

warnings.filterwarnings("ignore")

# ------------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------------
CSV_PATH   = os.path.join(os.path.dirname(__file__), "supermarket_sales.csv")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output_charts")
os.makedirs(OUTPUT_DIR, exist_ok=True)

PALETTE = ["#3b82d4", "#7c5cd8", "#10b981", "#f59e0b", "#ef4444", "#6366f1"]
sns.set_theme(style="whitegrid", palette=PALETTE)
plt.rcParams.update({"figure.dpi": 120, "font.size": 10})


# ------------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------------
def save(fig, name):
    path = os.path.join(OUTPUT_DIR, name)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print("  Chart saved -> " + path)


def section(title):
    bar = "=" * 60
    print("\n" + bar + "\n  " + title + "\n" + bar)


# ==================================================================
# STEP 1 - LOAD DATA
# ==================================================================
section("STEP 1 - Load Dataset")

df = pd.read_csv(CSV_PATH)
print("  Rows : " + str(len(df)))
print("  Cols : " + str(len(df.columns)))
print("\n  First 5 rows:")
print(df.head().to_string(index=False))
print("\n  Column dtypes:")
print(df.dtypes.to_string())


# ==================================================================
# STEP 2 - DATA QUALITY CHECK
# ==================================================================
section("STEP 2 - Data Quality Check")

# Missing values
missing = df.isnull().sum()
print("\n  Missing values per column:")
print(missing[missing >= 0].to_string())

# Duplicate rows
dups = df.duplicated().sum()
print("\n  Duplicate rows  : " + str(dups))

# Negative / zero quantities or prices
neg_qty   = (df["Quantity"]    <= 0).sum()
neg_price = (df["Unit price"]  <= 0).sum()
print("  Invalid Qty     : " + str(neg_qty))
print("  Invalid Price   : " + str(neg_price))

# Rating range check
out_range = ((df["Rating"] < 1) | (df["Rating"] > 10)).sum()
print("  Ratings out of [1-10]: " + str(out_range))

# Parse date
df["Date"] = pd.to_datetime(df["Date"])
print("\n  Date range: " + str(df["Date"].min().date()) +
      "  to  " + str(df["Date"].max().date()))


# ==================================================================
# STEP 3 - FEATURE ENGINEERING
# ==================================================================
section("STEP 3 - Feature Engineering")

# Recalculate Sales from raw columns to verify / create clean field
df["Sales"]   = (df["Quantity"] * df["Unit price"]).round(2)
df["Month"]   = df["Date"].dt.month_name()
df["Weekday"] = df["Date"].dt.day_name()

# Month order for plots
MONTH_ORDER   = ["January", "February", "March"]
WEEKDAY_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday",
                 "Friday", "Saturday", "Sunday"]

print("  New columns added: Sales, Month, Weekday")
print("  Total Sales (all): $" + f"{df['Sales'].sum():,.2f}")
print("  Avg Sales/tx     : $" + f"{df['Sales'].mean():,.2f}")


# ==================================================================
# STEP 4 - GROUPING & SUMMARISATION
# ==================================================================
section("STEP 4 - Group & Summarise")

# 4-a  Branch summary
branch_summary = (
    df.groupby("Branch")
      .agg(
          Total_Sales    =("Sales",      "sum"),
          Transactions   =("Invoice ID", "count"),
          Avg_Rating     =("Rating",     "mean"),
          Avg_Unit_Price =("Unit price", "mean"),
      )
      .round(2)
)
print("\n  -- Branch Summary --")
print(branch_summary.to_string())

# 4-b  Product line summary
product_summary = (
    df.groupby("Product line")
      .agg(
          Total_Sales  =("Sales",      "sum"),
          Transactions =("Invoice ID", "count"),
          Total_Qty    =("Quantity",   "sum"),
          Avg_Rating   =("Rating",     "mean"),
      )
      .round(2)
      .sort_values("Total_Sales", ascending=False)
)
print("\n  -- Product Line Summary --")
print(product_summary.to_string())

# 4-c  Payment method
payment_summary = (
    df.groupby("Payment")
      .agg(Total_Sales=("Sales", "sum"), Count=("Invoice ID", "count"))
      .round(2)
      .sort_values("Total_Sales", ascending=False)
)
print("\n  -- Payment Method Summary --")
print(payment_summary.to_string())

# 4-d  Customer type
cust_summary = (
    df.groupby("Customer type")
      .agg(Total_Sales=("Sales", "sum"), Count=("Invoice ID", "count"),
           Avg_Rating =("Rating", "mean"))
      .round(2)
)
print("\n  -- Customer Type Summary --")
print(cust_summary.to_string())

# 4-e  Gender
gender_summary = (
    df.groupby("Gender")
      .agg(Total_Sales=("Sales", "sum"), Count=("Invoice ID", "count"))
      .round(2)
)
print("\n  -- Gender Summary --")
print(gender_summary.to_string())

# 4-f  Monthly sales
monthly_sales = (
    df.groupby("Month")["Sales"]
      .sum()
      .reindex(MONTH_ORDER)
      .reset_index()
)

# 4-g  Branch x Category cross-tab
branch_cat = (
    df.groupby(["Branch", "Product line"])["Sales"]
      .sum()
      .unstack("Product line")
      .round(2)
)


# ==================================================================
# STEP 5 - VISUALISATIONS
# ==================================================================
section("STEP 5 - Visualisations")

# -- Chart 1: Total Sales by Branch (bar) --------------------------
fig, ax = plt.subplots(figsize=(6, 4))
bars = ax.bar(branch_summary.index, branch_summary["Total_Sales"],
              color=PALETTE[:3], edgecolor="white", width=0.5)
ax.bar_label(bars, fmt="$%.0f", padding=4, fontsize=9)
ax.set_title("Total Sales by Branch", fontweight="bold")
ax.set_xlabel("Branch")
ax.set_ylabel("Sales ($)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
fig.tight_layout()
save(fig, "01_sales_by_branch.png")

# -- Chart 2: Sales by Product Line (horizontal bar) ---------------
fig, ax = plt.subplots(figsize=(8, 5))
colors = PALETTE[:len(product_summary)]
ax.barh(product_summary.index, product_summary["Total_Sales"],
        color=colors, edgecolor="white")
for i, v in enumerate(product_summary["Total_Sales"]):
    ax.text(v + 200, i, f"${v:,.0f}", va="center", fontsize=9)
ax.set_title("Total Sales by Product Line", fontweight="bold")
ax.set_xlabel("Sales ($)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.invert_yaxis()
fig.tight_layout()
save(fig, "02_sales_by_product_line.png")

# -- Chart 3: Payment Method Distribution (pie) --------------------
fig, ax = plt.subplots(figsize=(6, 5))
wedges, texts, autotexts = ax.pie(
    payment_summary["Count"],
    labels=payment_summary.index,
    autopct="%1.1f%%",
    colors=PALETTE[:len(payment_summary)],
    startangle=140,
    pctdistance=0.75,
)
for t in autotexts:
    t.set_fontsize(10)
ax.set_title("Payment Method Distribution", fontweight="bold")
fig.tight_layout()
save(fig, "03_payment_distribution.png")

# -- Chart 4: Monthly Sales Trend (line) ---------------------------
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(monthly_sales["Month"], monthly_sales["Sales"],
        marker="o", linewidth=2.5, color=PALETTE[0], markersize=8)
for _, row in monthly_sales.iterrows():
    ax.annotate(f"${row['Sales']:,.0f}",
                (row["Month"], row["Sales"]),
                textcoords="offset points", xytext=(0, 10),
                ha="center", fontsize=9)
ax.set_title("Monthly Sales Trend", fontweight="bold")
ax.set_xlabel("Month")
ax.set_ylabel("Sales ($)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
fig.tight_layout()
save(fig, "04_monthly_sales_trend.png")

# -- Chart 5: Average Rating by Product Line (bar) -----------------
avg_rating = df.groupby("Product line")["Rating"].mean().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(8, 4))
bars = ax.bar(avg_rating.index, avg_rating.values,
              color=PALETTE[:len(avg_rating)], edgecolor="white", width=0.6)
ax.bar_label(bars, fmt="%.2f", padding=4, fontsize=9)
ax.set_ylim(0, 11)
ax.set_title("Average Customer Rating by Product Line", fontweight="bold")
ax.set_xlabel("Product Line")
ax.set_ylabel("Avg Rating (1-10)")
plt.xticks(rotation=20, ha="right")
fig.tight_layout()
save(fig, "05_avg_rating_by_product.png")

# -- Chart 6: Sales by Customer Type & Gender (grouped bar) --------
cg = df.groupby(["Customer type", "Gender"])["Sales"].sum().unstack("Gender")
fig, ax = plt.subplots(figsize=(6, 4))
cg.plot(kind="bar", ax=ax, color=PALETTE[:2], edgecolor="white", width=0.55)
ax.set_title("Sales by Customer Type & Gender", fontweight="bold")
ax.set_xlabel("Customer Type")
ax.set_ylabel("Sales ($)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.legend(title="Gender")
plt.xticks(rotation=0)
fig.tight_layout()
save(fig, "06_sales_customer_gender.png")

# -- Chart 7: Branch x Product Line Heatmap -----------------------
fig, ax = plt.subplots(figsize=(9, 4))
sns.heatmap(branch_cat, annot=True, fmt=",.0f", cmap="Blues",
            linewidths=0.5, ax=ax, cbar_kws={"label": "Sales ($)"})
ax.set_title("Sales Heatmap - Branch x Product Line", fontweight="bold")
ax.set_xlabel("Product Line")
ax.set_ylabel("Branch")
plt.xticks(rotation=25, ha="right")
fig.tight_layout()
save(fig, "07_branch_product_heatmap.png")

# -- Chart 8: Rating Distribution by Branch (box plot) -------------
fig, ax = plt.subplots(figsize=(7, 4))
branch_order   = sorted(df["Branch"].unique())
data_by_branch = [df[df["Branch"] == b]["Rating"].values for b in branch_order]
bp = ax.boxplot(data_by_branch, patch_artist=True,
                medianprops={"color": "black", "linewidth": 2})
ax.set_xticks(range(1, len(branch_order) + 1))
ax.set_xticklabels(branch_order)
for patch, color in zip(bp["boxes"], PALETTE):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
ax.set_title("Customer Rating Distribution by Branch", fontweight="bold")
ax.set_xlabel("Branch")
ax.set_ylabel("Rating (1-10)")
ax.set_ylim(0, 11)
fig.tight_layout()
save(fig, "08_rating_distribution_boxplot.png")

# -- Chart 9: Average Sales per Transaction by Weekday (bar) -------
weekday_avg = (
    df.groupby("Weekday")["Sales"]
      .mean()
      .reindex(WEEKDAY_ORDER)
      .dropna()
)
fig, ax = plt.subplots(figsize=(8, 4))
bars = ax.bar(weekday_avg.index, weekday_avg.values,
              color=PALETTE[4], edgecolor="white", width=0.6)
ax.bar_label(bars, fmt="$%.0f", padding=3, fontsize=9)
ax.set_title("Average Sales per Transaction by Weekday", fontweight="bold")
ax.set_xlabel("Day of Week")
ax.set_ylabel("Avg Sales ($)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.xticks(rotation=15, ha="right")
fig.tight_layout()
save(fig, "09_avg_sales_by_weekday.png")

# -- Chart 10: Quantity Sold per Product Line (pie) ----------------
qty_by_product = (
    df.groupby("Product line")["Quantity"]
      .sum()
      .sort_values(ascending=False)
)
fig, ax = plt.subplots(figsize=(7, 5))
ax.pie(qty_by_product.values, labels=qty_by_product.index,
       autopct="%1.1f%%", colors=PALETTE[:len(qty_by_product)],
       startangle=90, pctdistance=0.78)
ax.set_title("Quantity Sold by Product Line", fontweight="bold")
fig.tight_layout()
save(fig, "10_quantity_by_product.png")


# ==================================================================
# STEP 6 - BUSINESS INSIGHTS
# ==================================================================
section("STEP 6 - Business Insights")

top_branch   = branch_summary["Total_Sales"].idxmax()
top_product  = product_summary["Total_Sales"].idxmax()
top_payment  = payment_summary["Total_Sales"].idxmax()
top_month    = monthly_sales.set_index("Month")["Sales"].idxmax()
best_rated   = avg_rating.idxmax()
worst_rated  = avg_rating.idxmin()
best_weekday = weekday_avg.idxmax()
top_gender   = gender_summary["Total_Sales"].idxmax()
top_cust     = cust_summary["Total_Sales"].idxmax()

sep = "  " + "-" * 50
insights_lines = [
    "",
    "  +====================================================+",
    "  |      SUPERMARKET SALES - BUSINESS INSIGHTS         |",
    "  +====================================================+",
    "",
    "  [SALES PERFORMANCE]",
    sep,
    f"  Total Revenue        : ${df['Sales'].sum():>12,.2f}",
    f"  Total Transactions   : {len(df):>12,}",
    f"  Average Sale Value   : ${df['Sales'].mean():>12,.2f}",
    f"  Highest Single Sale  : ${df['Sales'].max():>12,.2f}",
    "",
    "  [BRANCH ANALYSIS]",
    sep,
    f"  Top Performing Branch: Branch {top_branch}",
    f"    Revenue    = ${branch_summary.loc[top_branch, 'Total_Sales']:,.2f}",
    f"    Avg Rating = {branch_summary.loc[top_branch, 'Avg_Rating']:.2f}",
    "",
    "  [PRODUCT LINE ANALYSIS]",
    sep,
    f"  Best-Selling Line    : {top_product}",
    f"    Revenue  = ${product_summary.loc[top_product, 'Total_Sales']:,.2f}",
    f"  Highest Rated Line   : {best_rated}  (avg {avg_rating[best_rated]:.2f}/10)",
    f"  Lowest  Rated Line   : {worst_rated} (avg {avg_rating[worst_rated]:.2f}/10)",
    f"    Recommendation: Improve quality/service for '{worst_rated}'",
    "",
    "  [PAYMENT METHOD ANALYSIS]",
    sep,
    f"  Most Used Method     : {top_payment}",
    f"    Revenue  = ${payment_summary.loc[top_payment, 'Total_Sales']:,.2f}",
    f"    Recommendation: Offer cashback / loyalty points on {top_payment}",
    "",
    "  [CUSTOMER ANALYSIS]",
    sep,
    f"  Top Customer Segment : {top_cust}",
    f"  Top Spending Gender  : {top_gender}",
    f"    Recommendation: Target {top_gender} customers with promotions",
    "",
    "  [TIME ANALYSIS]",
    sep,
    f"  Best Month           : {top_month}",
    f"    Revenue  = ${monthly_sales.set_index('Month')['Sales'][top_month]:,.2f}",
    f"  Best Weekday Avg Sale: {best_weekday}",
    f"    Avg Sale = ${weekday_avg[best_weekday]:,.2f}",
    f"    Recommendation: Run targeted deals on {best_weekday}",
    "",
    f"  All 10 charts saved to: {OUTPUT_DIR}",
    "",
]

insights = "\n".join(insights_lines)
print(insights)

# Save insights to text file
report_path = os.path.join(OUTPUT_DIR, "business_insights.txt")
with open(report_path, "w", encoding="utf-8") as f:
    f.write(insights)
print("  Report saved -> " + report_path + "\n")

section("ANALYSIS COMPLETE")
