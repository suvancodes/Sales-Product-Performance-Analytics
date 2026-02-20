# Sales & Product Performance Analytics

Industry-ready analytics project focused on measuring **sales performance**, **product contribution**, and business **KPIs** to support data-driven decision-making. The repository is structured to be maintainable, reproducible, and easy for analysts and developers to extend.

---

## Overview

This project is designed to analyze sales and product performance to answer questions such as:

- Which products drive the most revenue and profit?
- How do sales trend over time (daily/weekly/monthly/quarterly)?
- Which categories/segments contribute most to growth?
- Are there seasonality patterns or demand spikes?
- What is the performance across regions/channels (if applicable)?

**Goal:** Provide a clean analytics workflow (data → transformations → KPIs → reporting) that can be used as a foundation for real-world BI/analytics initiatives.

---

## Key Features

- KPI framework for business performance tracking (**Revenue, Units Sold, Profit, Margin %, AOV, Growth %**)
- Product analytics (top/bottom products, **Pareto/80-20**, contribution analysis)
- Trend and period comparisons (MoM/YoY where data allows)
- Data-quality checks (missing values, invalid dates, negative quantities, duplicates)
- Reusable transformations and clear separation of raw vs processed data
- Dashboard-ready outputs (clean tables/views for BI tools)

---

## Tech Stack (Current Repo)

- **Language / Runtime:** Node.js + TypeScript
- **API / App Framework:** Express
- **Package Manager:** npm
- **Data Storage:** CSV files (see `DATA/`)
- **Environment:** local Node runtime (no containerization currently)

> Note: The current repository contains a TypeScript/Express starter under `project-name/`. The analytics pipeline/metrics implementation can be layered on top of this structure as the project evolves.

---

## 📁 Repository Structure

```

E-Commerce-Sales-Intelligence-Dashboard/
│
├── DATA/                         # All datasets
│   ├── Amazon Sale Report.csv
│   ├── International Sale Report.csv
│   
│   
│   
│
├── script/                          # Python source code
│   ├── etl.py                    # ETL pipeline (merge + clean)
│   ├── matrix.py          # make all KPI for this project
│   ├── logger.py
│   └── exception.py
│
├── sql/                          # SQL scripts
│   └── analysis_queries.sql      # All SQL queries (KPIs + joins)
│
├── analysis/                     # Jupyter notebooks
│   └── eda.ipynb
│
├── KPI/                      # Outputs
│   |── Results and images/                   # Dashboard screenshots / charts
|   
│
├── README.md                     # Project documentation
├── requirements.txt              # Python dependencies
└── .gitignore

```
---

## Data

### Dataset
- **Location:** `DATA/`
- **Format:** CSV
- **Example file:** `DATA/May-2022.csv`

### Example Fields (from current CSV)
Based on `DATA/May-2022.csv`, the dataset includes columns such as:

- `Sku`, `Style Id`, `Catalog`, `Category`
- `Weight`, `TP`
- Multiple price columns (e.g., `Ajio MRP`, `Amazon MRP`, `Flipkart MRP`, `Myntra MRP`, etc.)

> Tip: If you later add transaction-level order data (order_id, order_date, qty, revenue, cost), you can compute the full KPI suite (profit, margin, AOV, growth) directly.

---

## Metrics (KPIs)

Typical KPIs intended for this project:

- **Revenue** = Σ (Quantity × Unit Price)
- **Units Sold** = Σ Quantity
- **Profit** = Revenue − Cost
- **Profit Margin %** = Profit / Revenue
- **Average Order Value (AOV)** = Revenue / #Orders
- **Growth % (MoM / YoY)** = (Current − Previous) / Previous

---

## How to Run (Developer Setup)

### 1) Clone the repository
```bash
git clone https://github.com/suvancodes/Sales-Product-Performance-Analytics.git
cd Sales-Product-Performance-Analytics
```

### 2) Install dependencies (TypeScript/Node app)
The runnable app currently lives under `project-name/`.

```bash
cd project-name
npm install
```

### 3) Start the app
```bash
npm start
```

By default, the server starts on port `3000` (or `PORT` env var if set).

---

## Outputs

This repository currently includes:
- Raw dataset files in `DATA/`

Planned outputs as the analytics layer is implemented:
- Cleaned/curated datasets (e.g., `data/processed/`)
- KPI tables for dashboarding (daily/monthly KPIs)
- Product performance tables (top products, category contribution)
- Visualizations saved to `reports/`
- Dashboard files in `dashboards/`

---

## Example Insights (Replace with real findings)

Once the KPI and transformation layer is implemented and executed, document 3–6 concrete findings here, for example:

- Top 20% of products contribute ~78% of total revenue (Pareto effect).
- Highest growth category: Category X (+18% MoM) driven by seasonal demand.
- Margin compression observed in Region Y due to discounting.

---

## Testing

No automated test suite is configured at the repository root currently.

Suggested next step:
- Add unit tests for metric calculations and data-quality rules once the analytics pipeline is implemented.

---

## Roadmap

- [ ] Implement transformations and KPI computations from the CSV dataset(s)
- [ ] Add automated data validation (pandera / Great Expectations)
- [ ] Add reproducible outputs (processed datasets + KPI tables)
- [ ] Add BI-ready exports and documented dashboard screenshots
- [ ] Add trend analysis (MoM/YoY) and seasonality detection
- [ ] Add forecasting (Prophet / ARIMA) for demand trends

---

## Contributing

Contributions are welcome.

1. Fork the repository  
2. Create a feature branch: `git checkout -b feature/my-change`  
3. Commit changes: `git commit -m "Add: ..."`  
4. Push: `git push origin feature/my-change`  
5. Open a Pull Request

---

## License

No license file is included currently.

Recommended for portfolio/open-source: **MIT License**.

---

## Contact

**Author:** Suvan (`@suvancodes`)  
**Repository:** https://github.com/suvancodes/Sales-Product-Performance-Analytics

For feedback or collaboration, please open an issue in this repository.
