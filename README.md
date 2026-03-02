# 📊 E-Commerce Sales & Customer Insights Analytics System

A production-style end-to-end analytics system built using **Python, MySQL, SQL, and Pandas** to process, clean, analyze, and generate business KPIs from 150K+ e-commerce transactions.

This project demonstrates structured ETL design, automated KPI generation, SQL analytics, and database integration.

---

# 🚀 Project Overview

This system performs:

* Multi-source data ingestion (Amazon + International sales)
* Data cleaning & transformation
* Feature engineering
* Master dataset creation
* Automated KPI generation
* Product & geographic analytics
* Advanced analytical metrics
* MySQL database loading
* SQL-based business queries

The goal is to convert raw transactional data into structured, business-ready analytics.

---

# 🏗️ System Architecture

Raw Amazon Data + International Sales
↓
Data Cleaning & Standardization (Pandas)
↓
Master Dataset Creation
↓
Feature Engineering (Year, Month, Day)
↓
KPI Engine (Revenue, Growth, Pareto, AOV, etc.)
↓
MySQL Database Loading
↓
SQL-Based Analytics

---

# 🛠️ Tech Stack

* Python (Pandas, NumPy)
* MySQL
* SQL (GROUP BY, JOIN, Subqueries)
* SQLAlchemy
* Matplotlib & Seaborn
* Logging & Custom Exception Handling
* Environment Variables (.env)

---

# 📂 Project Structure

```
DATA/
    Amazon Sale Report.csv
    International Sale Report.csv
    master_sales.csv
    cleaned_master_sales.csv

Script/
    etl.py
    matrix.py
    loder_sql.py
    logger.py
    exception.py

sql/
    analysis_queries.sql

KPI/
    Revenue_Metrics/
    Monthly_Analysis/
    Product Analytics/
    Geographic_Analysis/
    Advanced_Analytical_Features/

.env
README.md
```

---

# 🔄 ETL Pipeline (etl.py)

### Data Ingestion

* Load Amazon dataset
* Load International dataset
* Standardize column names
* Normalize SKU format

### Data Transformation

* Convert revenue & quantity to numeric
* Convert order_date to datetime
* Add `source` column
* Merge datasets using `pd.concat()`
* Remove duplicates

### Data Cleaning

* Handle missing values
* Remove invalid rows (revenue ≤ 0, quantity ≤ 0)
* Extract:

  * Year
  * Month
  * Day

Cleaned dataset saved as:

```
DATA/cleaned_master_sales.csv
```

---

# 📊 KPI Engine (matrix.py)

Automated generation of business KPIs and visualization outputs.

## Revenue Metrics

* Total Revenue
* Total Orders
* Total Quantity Sold
* Average Order Value (AOV)
* Revenue by Source

Output:

```
KPI/Revenue_Metrics/
```

---

## Monthly Analysis

* Monthly Revenue
* Monthly Quantity Sold
* Monthly Growth %
* Revenue Trend Line

Output:

```
KPI/Monthly_Analysis/
```

---

## Product Analytics

* Top 10 SKUs by Revenue
* Top 10 SKUs by Quantity
* Revenue Contribution %
* Pareto (80/20 Rule)
* Cumulative Revenue Percentage

Output:

```
KPI/Product Analytics/
```

---

## Geographic Analysis

* Revenue by Country
* Quantity by Country
* Revenue % Contribution by Country

Output:

```
KPI/Geographic_Analysis/
```

---

## Advanced Analytical Features

* Revenue by Day of Week
* Rolling 7-Day Revenue
* Revenue Distribution (Histogram + Boxplot)
* Top 20% SKU Contribution

Output:

```
KPI/Advanced_Analytical_Features/
```

---

# 🗄️ MySQL Integration (loder_sql.py)

Uses `.env` file for secure credentials:

```
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DB_NAME=
```

Loads cleaned dataset into MySQL:

```python
df.to_sql("master_sales", engine, if_exists="replace", index=False)
```

---

# 📈 Example SQL Queries

## Monthly Revenue

```sql
SELECT
    MONTH(order_date) AS month,
    SUM(revenue) AS monthly_revenue
FROM master_sales
GROUP BY MONTH(order_date)
ORDER BY month;
```

## Revenue by Country

```sql
SELECT
    country,
    SUM(revenue) AS total_revenue
FROM master_sales
GROUP BY country
ORDER BY total_revenue DESC;
```

## Revenue by Source

```sql
SELECT
    source,
    SUM(revenue) AS total_revenue
FROM master_sales
GROUP BY source;
```

## Top Products via JOIN

```sql
CREATE TABLE products AS
SELECT DISTINCT
    sku,
    'General' AS category,
    'NA' AS size,
    'NA' AS color
FROM master_sales;

SELECT
    m.sku,
    p.category,
    SUM(m.revenue) AS total_revenue
FROM master_sales m
JOIN products p
ON m.sku = p.sku
GROUP BY m.sku, p.category
ORDER BY total_revenue DESC
LIMIT 10;
```

---

# 🎯 Business Value Delivered

* Revenue trend monitoring
* Product prioritization using Pareto analysis
* Geographic performance insights
* Growth tracking
* AOV monitoring
* Rolling revenue smoothing
* Business-ready KPI exports
* SQL-driven reporting layer

---

# 💼 Skills Demonstrated

* End-to-end ETL design
* Data cleaning & validation
* Feature engineering
* Business KPI modeling
* Python–MySQL integration
* SQL aggregation & joins
* Automated analytics reporting
* Structured logging & exception handling

---

# 👨‍💻 Author

Suvankar Payra
Data Analyst | Python | SQL | ETL & KPI Analytics
GitHub: [https://github.com/suvancodes](https://github.com/suvancodes)

---
