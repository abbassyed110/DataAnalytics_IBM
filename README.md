<h1 align="center">🛒 Supermarket Sales Analytics</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/Plotly-Interactive-3F4F75?style=for-the-badge&logo=plotly&logoColor=white"/>
  <img src="https://img.shields.io/badge/pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white"/>
  <img src="https://img.shields.io/badge/IBM-Data%20Analytics-054ADA?style=for-the-badge&logo=ibm&logoColor=white"/>
</p>

<p align="center">
  <strong>An end-to-end data analytics project analysing 500 supermarket transactions across 3 branches —<br/>
  featuring 10 interactive charts, KPI dashboards, and actionable business insights.</strong>
</p>

<p align="center">
  <a href="https://github.com/abbassyed110/DataAnalytics_IBM/tree/main/supermarket_sales">📁 View Project Files</a> •
  <a href="https://github.com/abbassyed110/DataAnalytics_IBM/blob/main/supermarket_sales/AbbasAli_SupermarketSales.ipynb">📓 Open Notebook</a> •
  <a href="https://github.com/abbassyed110/DataAnalytics_IBM/blob/main/supermarket_sales/AbbasAli_ProjectReport.docx">📄 Project Report</a>
</p>

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Dataset](#-dataset)
- [Project Structure](#-project-structure)
- [Analysis Pipeline](#-analysis-pipeline)
- [Visualisations](#-visualisations)
- [Key Findings](#-key-findings)
- [Business Recommendations](#-business-recommendations)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Submission Files](#-submission-files)
- [Author](#-author)

---

## 🔍 Overview

This project performs a complete **data analytics pipeline** on a synthetic supermarket sales dataset — from raw CSV ingestion to an interactive Streamlit web dashboard.

**Business questions answered:**

| # | Question |
|---|---|
| 1 | Which branch generates the highest revenue? |
| 2 | Which product lines are the most profitable? |
| 3 | What payment methods do customers prefer? |
| 4 | How do sales vary by month and day of week? |
| 5 | Do Member customers spend more than Normal customers? |

---

## 📊 Dataset

| Property | Detail |
|---|---|
| **Source** | Synthetically generated via `generate_dataset.py` |
| **Rows** | 500 transactions |
| **Columns** | 16 features |
| **Period** | January 1 – March 31, 2019 |
| **Branches** | A — Yangon · B — Naypyitaw · C — Mandalay |
| **File** | `supermarket_sales/supermarket_sales.csv` |

<details>
<summary><b>📋 Column Reference (click to expand)</b></summary>

| Column | Type | Description |
|---|---|---|
| `Invoice ID` | string | Unique transaction identifier |
| `Branch` | string | Store branch (A / B / C) |
| `City` | string | City of the branch |
| `Customer type` | string | Member or Normal |
| `Gender` | string | Male or Female |
| `Product line` | string | Product category (6 types) |
| `Unit price` | float | Price per unit ($) |
| `Quantity` | int | Number of items purchased |
| `Tax 5%` | float | 5% tax applied on the sale |
| `Total` | float | Total amount including tax |
| `Date` | date | Transaction date |
| `Time` | time | Transaction time (HH:MM) |
| `Payment` | string | Ewallet / Cash / Credit card |
| `cogs` | float | Cost of goods sold |
| `gross income` | float | Gross income |
| `Rating` | float | Customer satisfaction score (1–10) |

</details>

---

## 📁 Project Structure

```
DataAnalytics_IBM/
│
└── supermarket_sales/
    ├── 📓 AbbasAli_SupermarketSales.ipynb   ← Jupyter Notebook (submission)
    ├── 📄 AbbasAli_ProjectReport.docx        ← Full project report (submission)
    ├── 📋 README.md                          ← Project README (submission)
    ├── 📦 requirements.txt                   ← Python dependencies (submission)
    │
    ├── 🖥️  app.py                            ← Streamlit interactive dashboard
    ├── 🐍 supermarket_analytics.py           ← Static analysis + 10 PNG charts
    ├── 🔧 generate_dataset.py                ← Synthetic dataset generator
    ├── 📊 supermarket_sales.csv              ← Dataset (500 rows)
    ├── 📊 supermarket_sales.xlsx             ← Excel version
    │
    └── output_charts/                        ← Saved chart images
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

## ⚙️ Analysis Pipeline

```
Step 1 ── Load Data          →  Read CSV, inspect shape, dtypes, preview rows
Step 2 ── Quality Check      →  Missing values · Duplicates · Invalid ranges
Step 3 ── Feature Engineering→  Derive Sales, Month, Weekday columns
Step 4 ── Summarise          →  Group by Branch · Product · Payment · Gender
Step 5 ── Visualise          →  10 charts: bar · pie · line · heatmap · boxplot
Step 6 ── Insights           →  Quantitative recommendations from aggregated data
```

---

## 📈 Visualisations

| # | Chart Title | Chart Type |
|---|---|---|
| 1 | Total Sales by Branch | Vertical Bar |
| 2 | Sales by Product Line | Horizontal Bar |
| 3 | Payment Method Distribution | Donut Pie |
| 4 | Monthly Sales Trend (Jan–Mar) | Line |
| 5 | Average Customer Rating by Product Line | Bar |
| 6 | Sales by Customer Type & Gender | Grouped Bar |
| 7 | Branch × Product Line Revenue | Heatmap |
| 8 | Rating Distribution by Branch | Box Plot |
| 9 | Avg Sale per Transaction by Weekday | Bar |
| 10 | Quantity Sold by Product Line | Donut Pie |

> 🖥️ All 10 charts are available **interactively** in the Streamlit dashboard (`app.py`) and as **static PNGs** in `output_charts/`.

---

## 💡 Key Findings

> Based on analysis of **500 transactions** across **3 branches** over **3 months**.

- 💰 **Total revenue** exceeded **$50,000** across all branches
- 🏆 **Branch A (Yangon)** leads marginally in total revenue
- 📦 **Food & Beverages** and **Fashion Accessories** are the top product lines
- 💳 **Ewallet** is the most popular payment method (~33% of transactions)
- 🎟️ **Member customers** spend more per transaction than Normal customers
- 📅 **January** was the highest-revenue month of the quarter
- 📆 **Saturday** shows the highest average sale value per transaction

---

## 🎯 Business Recommendations

| # | Recommendation |
|---|---|
| 1 | 🏪 **Branch Strategy** — Identify and replicate what drives Branch A's revenue edge |
| 2 | 🎟️ **Membership Growth** — Convert Normal customers via sign-up incentives |
| 3 | 💳 **Ewallet Rewards** — Cashback/loyalty points to reinforce digital payments |
| 4 | 📦 **January Stock-Up** — Pre-stock high-demand categories before peak month |
| 5 | ⭐ **Quality Improvement** — Address service gaps in the lowest-rated product line |
| 6 | 🗓️ **Weekend Promotions** — Run targeted deals on Saturdays (peak spend day) |

---

## 🛠️ Tech Stack

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white"/>
  <img src="https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white"/>
  <img src="https://img.shields.io/badge/Matplotlib-11557c?style=flat-square"/>
  <img src="https://img.shields.io/badge/Seaborn-4C72B0?style=flat-square"/>
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/Jupyter-F37626?style=flat-square&logo=jupyter&logoColor=white"/>
</p>

| Library | Version | Role |
|---|---|---|
| Python | 3.8+ | Core language |
| pandas | ≥ 1.5 | Data loading, cleaning, grouping |
| matplotlib | ≥ 3.6 | Static chart generation |
| seaborn | ≥ 0.12 | Statistical visualisations |
| plotly | ≥ 5.18 | Interactive charts |
| Streamlit | ≥ 1.32 | Web dashboard |
| openpyxl | ≥ 3.0 | Excel file support |

---

## 🚀 Quick Start

### 1 · Clone the repository

```bash
git clone https://github.com/abbassyed110/DataAnalytics_IBM.git
cd DataAnalytics_IBM/supermarket_sales
```

### 2 · Create & activate a virtual environment

```bash
# Create
python -m venv .venv

# Activate — Windows
.venv\Scripts\Activate.ps1

# Activate — macOS / Linux
source .venv/bin/activate
```

### 3 · Install dependencies

```bash
pip install -r requirements.txt
```

### 4 · Generate the dataset *(skip if CSV already exists)*

```bash
python generate_dataset.py
```

### 5 · Run the project

| Mode | Command |
|---|---|
| 📓 Jupyter Notebook | `jupyter notebook AbbasAli_SupermarketSales.ipynb` |
| 🐍 Static analysis + charts | `python supermarket_analytics.py` |
| 🖥️ Streamlit dashboard | `.venv\Scripts\python.exe -m streamlit run app.py` |

> ⚠️ **Always launch Streamlit via the venv Python** (`.venv\Scripts\python.exe -m streamlit run app.py`) to avoid `ModuleNotFoundError: No module named 'plotly'`.

---

## 📂 Submission Files

| File | Format | Description |
|---|---|---|
| `AbbasAli_SupermarketSales.ipynb` | `.ipynb` | Complete project code — Jupyter Notebook |
| `requirements.txt` | `.txt` | Python library dependencies |
| `AbbasAli_ProjectReport.docx` | `.docx` | Full project documentation |
| `README.md` | `.md` | This file — project overview & run guide |

---

## 👤 Author

**Abbas Ali**
📧 abbassayed7799@gmail.com
🎓 IBM Data Analytics Course
🔗 [github.com/abbassyed110](https://github.com/abbassyed110)

---

<p align="center">
  <sub>Built with Python · pandas · plotly · Streamlit · IBM Data Analytics Programme</sub>
</p>
