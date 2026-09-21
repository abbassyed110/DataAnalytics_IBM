"""
generate_dataset.py
-------------------
Generates a realistic synthetic supermarket sales CSV with 500 transactions.
Run once before supermarket_analytics.py.
"""

import csv
import random
from datetime import datetime, timedelta

random.seed(42)

BRANCHES   = ["A", "B", "C"]
CITIES     = {"A": "Yangon", "B": "Naypyitaw", "C": "Mandalay"}
CATEGORIES = ["Health and beauty", "Electronic accessories",
               "Home and lifestyle", "Sports and travel",
               "Food and beverages", "Fashion accessories"]
GENDERS    = ["Male", "Female"]
CUST_TYPES = ["Member", "Normal"]
PAYMENTS   = ["Ewallet", "Cash", "Credit card"]

UNIT_PRICES = {
    "Health and beauty":       (10.0,  90.0),
    "Electronic accessories":  (15.0,  95.0),
    "Home and lifestyle":      (12.0,  85.0),
    "Sports and travel":       (10.0,  80.0),
    "Food and beverages":      (5.0,   60.0),
    "Fashion accessories":     (8.0,   88.0),
}

START_DATE = datetime(2019, 1, 1)
END_DATE   = datetime(2019, 3, 31)

def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

def random_time():
    h = random.randint(10, 20)
    m = random.randint(0, 59)
    return f"{h:02d}:{m:02d}"

rows = []
for i in range(1, 501):
    branch    = random.choice(BRANCHES)
    city      = CITIES[branch]
    category  = random.choice(CATEGORIES)
    gender    = random.choice(GENDERS)
    cust_type = random.choice(CUST_TYPES)
    payment   = random.choice(PAYMENTS)
    qty       = random.randint(1, 10)
    lo, hi    = UNIT_PRICES[category]
    unit_price = round(random.uniform(lo, hi), 2)
    sales      = round(qty * unit_price, 2)
    tax        = round(sales * 0.05, 2)
    total      = round(sales + tax, 2)
    cogs       = sales
    gross_inc  = tax
    rating     = round(random.uniform(4.0, 10.0), 1)
    date       = random_date(START_DATE, END_DATE).strftime("%m/%d/%Y")
    time       = random_time()
    invoice_id = f"{random.randint(100,999)}-{random.randint(10,99)}-{random.randint(1000,9999)}"

    rows.append([
        invoice_id, branch, city, cust_type, gender, category,
        unit_price, qty, tax, total, date, time, payment,
        cogs, gross_inc, rating
    ])

HEADER = [
    "Invoice ID", "Branch", "City", "Customer type", "Gender",
    "Product line", "Unit price", "Quantity", "Tax 5%", "Total",
    "Date", "Time", "Payment", "cogs", "gross income", "Rating"
]

with open("supermarket_sales/supermarket_sales.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(HEADER)
    writer.writerows(rows)

print("Dataset generated -> supermarket_sales/supermarket_sales.csv  (500 rows)")
