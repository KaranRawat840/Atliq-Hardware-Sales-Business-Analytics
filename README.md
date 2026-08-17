# Atliq-Hardware-Sales-Business-Analytics
End-to-end SQL + Python analysis of a consumer electronics company's sales data, answering ad-hoc business requests from company leadership.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458)
![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-11557c)

---

## 📌 Project Overview

Atliq Hardware sells peripherals, notebooks, desktops, storage, and networking
products across 8+ countries in APAC, EU, NA, and LATAM. This project answers 10
business questions posed by leadership — spanning market presence, product growth,
cost analysis, discounting behavior, seasonal trends, and channel performance —
using a relational database of ~1 million sales transactions (FY2020–FY2021).

**Tech stack:** MySQL (database) → SQLAlchemy + pandas (analysis) → Matplotlib
(visualization)

---

## 🗃️ Database Schema

The `gdb023` database has 6 tables:

| Table | Purpose |
|---|---|
| `dim_customer` | Customer name, platform, channel, market, region |
| `dim_product` | Product name, division, segment, category, variant |
| `fact_gross_price` | Gross price per product, per fiscal year |
| `fact_manufacturing_cost` | Manufacturing cost per product, per fiscal year |
| `fact_pre_invoice_deductions` | Pre-invoice discount % per customer, per fiscal year |
| `fact_sales_monthly` | Monthly sold quantity per product, per customer |

---

## ❓ Business Questions Answered

1. Which APAC markets does Atliq Exclusive operate in?
2. How did unique product count change from 2020 to 2021?
3. What are the unique product counts by segment?
4. Which segment grew the most in unique products, 2020→2021?
5. Which products have the highest/lowest manufacturing cost?
6. Who are the top 5 customers by pre-invoice discount % (India, FY2021)?
7. What are Atliq Exclusive's monthly gross sales?
8. Which fiscal quarter of 2020 had the highest sold quantity?
9. Which channel contributes most to FY2021 gross sales?
10. What are the top 3 products per division by sold quantity (FY2021)?

---

## 📊 Key Findings

- **Catalog growth:** Active product count grew **36%** (245 → 334) from FY2020 to FY2021, led by the Accessories segment (+34 SKUs).
- **COVID impact, visible in the data:** Atliq Exclusive's monthly gross sales collapsed to under $1M/month between March–August 2020, then rebounded to a **$20.46M peak in November 2020**.
- **Channel concentration:** Retailers drive **73%** of FY2021 gross sales, versus just 15% from Atliq's own Direct channel.
- **Cost spread:** Manufacturing cost ranges from **$0.89** (wired mice) to **$99.54** (AQ Gen X notebook) — a >100x spread across the catalog.
- **Discount leaders:** Flipkart and major Indian electronics retailers (Viveks, Ezone, Croma) receive the steepest pre-invoice discounts (~30%) in FY2021.

---

## 📈 Visuals
![monthly gross sale](https://github.com/KaranRawat840/Atliq-Hardware-Sales-Business-Analytics/blob/main/monthly%20gross%20sales.png)
*Atliq Exclusive's monthly gross sales, showing the COVID-19 dip and festive-season rebound.*

![Channel Contribution to Gross Sales - FY2021](https://github.com/KaranRawat840/Atliq-Hardware-Sales-Business-Analytics/blob/main/Channel%20%20Contribution%20to%20Gross%20Sales%20-%20FY2021.png)
*FY2021 gross sales contribution by channel.*

![Unique product count by Segment](https://github.com/KaranRawat840/Atliq-Hardware-Sales-Business-Analytics/blob/main/Unique%20product%20count%20by%20Segment.png)
*Unique product count by segment.*

---

## 🛠️ How to Reproduce This

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/atliq-hardware-sales-analysis.git
cd atliq-hardware-sales-analysis

# 2. Install dependencies
pip install pandas sqlalchemy pymysql matplotlib

# 3. Import the database (dump not included — see /data/README for source)
mysql -u root -p < data/atliq_hardware_db.sql

# 4. Run the analysis
python scripts/analysis.py
```

Connection setup used throughout:
```python
from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://root:yourpw@localhost/gdb023")
```

---

## 📂 Repo Structure

```
atliq-hardware-sales-analysis/
├── README.md
├── notebooks/
│   └── analysis.ipynb
├── scripts/
│   └── analysis.py
├── charts/
│   ├── q3_segment_products.png
│   ├── q7_monthly_sales.png
│   └── q9_channel_pie.png
└── data/
    └── (schema description — raw data not included)
```

---

## 🙋 About This Project

Built as a hands-on SQL + pandas practice project to work through realistic
ad-hoc business requests: multi-table joins, fiscal-year logic, ranking within
groups, and picking the right chart for each type of question.

Connect with me on [LinkedIn](#) or check out my other projects on
[my GitHub profile](#).
