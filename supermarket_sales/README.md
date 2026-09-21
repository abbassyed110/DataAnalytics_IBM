# Supermarket Sales Analytics

**Author:** Abbas Ali
**Course:** IBM Data Analytics
**Dataset:** Synthetic supermarket transactions — 500 rows, Jan–Mar 2019

---

## Project Description

An end-to-end Python data analytics project that analyses 500 supermarket sales transactions across three branches (Yangon, Naypyitaw, Mandalay). The project covers data loading, quality checking, feature engineering, statistical summarisation, 10 analytical visualisations, and a Streamlit interactive dashboard.

**Key questions answered:**
- Which branch generates the most revenue?
- Which product lines are the most profitable?
- What payment methods do customers prefer?
- How do sales vary by month and day of week?
- Do Member customers spend more than Normal customers?

---

## Dataset

| Property | Value |
|---|---|
| Source | Synthetically generated (`generate_dataset.py`) |
| Rows | 500 transactions |
| Columns | 16 |
| Date range | January 1 – March 31, 2019 |
| Branches | A (Yangon), B (Naypyitaw), C (Mandalay) |
| File | `supermarket_sales.csv` |

**Dataset columns:** Invoice ID, Branch, City, Customer type, Gender, Product line, Unit price, Quantity, Tax 5%, Total, Date, Time, Payment, cogs, gross income, Rating

---

## Project Structure

```
supermarket_sales/
├── AbbasAli_SupermarketSales.ipynb  ← Jupyter Notebook (submission)
├── AbbasAli_ProjectReport.docx      ← Full project report (submission)
├── README.md                        ← This file (submission)
├── requirements.txt                 ← Python dependencies (submission)
│
├── app.py                           ← Streamlit interactive dashboard
├── supermarket_analytics.py         ← Full analysis pipeline (static charts)
├── generate_dataset.py              ← Dataset generator (run once)
├── supermarket_sales.csv            ← Dataset (generated)
├── supermarket_sales.xlsx           ← Excel version of dataset
└── output_charts/                   ← Saved PNG charts + business_insights.txt
    ├── 01_sales_by_branch.png
    ├── 02_sales_by_product_line.png
    ├── 03_payment_distribution.png
    ├── 04_monthly_sales_trend.png
    ├── 05_avg_rating_by_product.png
    ├── 06_sales_customer_gender.png
    ├── 07_branch_product_heatmap.png
    ├── 08_rating_distribution_boxplot.png
    ├── 09_avg_sales_by_weekday.png
    ├── 10_quantity_by_product.png
    └── business_insights.txt
```

---

## Technologies Used

| Technology | Version | Purpose |
|---|---|---|
| Python | 3.8+ | Core programming language |
| pandas | ≥ 1.5 | Data loading, cleaning, grouping, summarisation |
| matplotlib | ≥ 3.6 | Static chart generation |
| seaborn | ≥ 0.12 | Statistical visualisations |
| plotly | ≥ 5.18 | Interactive charts in Streamlit |
| Streamlit | ≥ 1.32 | Interactive web dashboard |
| openpyxl | ≥ 3.0 | Excel file support |

---

## Setup & Run Instructions

### 1. Clone / download the project

```bash
# Navigate to the project folder
cd supermarket_sales
```

### 2. Create and activate a virtual environment

```bash
# Create venv
python -m venv .venv

# Activate (Windows)
.venv\Scripts\Activate.ps1

# Activate (macOS / Linux)
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate the dataset (if CSV is missing)

```bash
python generate_dataset.py
```

### 5a. Run the Jupyter Notebook

```bash
jupyter notebook AbbasAli_SupermarketSales.ipynb
```

### 5b. Run the static analysis script (generates 10 PNG charts)

```bash
python supermarket_analytics.py
```

### 5c. Launch the Streamlit interactive dashboard

```bash
# Always use the venv Python to avoid module-not-found errors
.venv\Scripts\python.exe -m streamlit run app.py
```

---

## Analysis Steps

| Step | Description |
|---|---|
| 1 | **Load** — Read CSV with pandas; inspect shape, dtypes, first rows |
| 2 | **Quality Check** — Missing values, duplicates, invalid quantities/prices, rating range |
| 3 | **Feature Engineering** — Derive `Sales`, `Month`, `Weekday` columns |
| 4 | **Summarise** — Group by Branch, Product Line, Payment, Customer Type, Gender |
| 5 | **Visualise** — 10 charts: bar, horizontal bar, pie, line, heatmap, box plot |
| 6 | **Insights** — Quantitative business recommendations from aggregated data |

---

## Charts Produced (10 total)

| # | Chart | Type |
|---|---|---|
| 1 | Total Sales by Branch | Vertical bar |
| 2 | Sales by Product Line | Horizontal bar |
| 3 | Payment Method Distribution | Donut pie |
| 4 | Monthly Sales Trend | Line |
| 5 | Average Rating by Product Line | Bar |
| 6 | Sales by Customer Type & Gender | Grouped bar |
| 7 | Branch × Product Line Revenue | Heatmap |
| 8 | Rating Distribution by Branch | Box plot |
| 9 | Avg Sale per Transaction by Weekday | Bar |
| 10 | Quantity Sold by Product Line | Donut pie |

---

## Key Findings

- **Total revenue** exceeded $50,000 across 500 transactions
- **Branch A (Yangon)** slightly leads in total revenue
- **Food & Beverages** and **Fashion Accessories** are the top product lines
- **Ewallet** is the most popular payment method (~33% of transactions)
- **Member customers** have a higher average spend than Normal customers
- **January** was the peak revenue month
- **Saturday** shows the highest average sale value per transaction

---

## Business Recommendations

1. Replicate top-branch strategies across underperforming branches
2. Convert Normal customers to Members through sign-up incentives
3. Offer Ewallet cashback/loyalty rewards to drive digital payment adoption
4. Pre-stock high-demand categories before January
5. Improve service quality for the lowest-rated product line
6. Run targeted promotions on Saturdays (peak spend day)

---

## Submission Files

| File | Description |
|---|---|
| `AbbasAli_SupermarketSales.ipynb` | Complete project code in Jupyter Notebook format |
| `requirements.txt` | Python library dependencies |
| `AbbasAli_ProjectReport.docx` | Full project documentation in Word format |
| `README.md` | This file — project overview and run instructions |
