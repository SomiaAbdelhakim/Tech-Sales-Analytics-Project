# 📊 Tech Sales Analytics Dashboard

## Overview

This project implements an end-to-end Data Engineering and Business Intelligence solution for a technology retail company.

The solution transforms raw sales data into a structured dimensional model using Python ETL and builds an interactive Power BI dashboard to analyze sales performance, customer behavior, product performance, and forecast accuracy.

---

## Project Objectives

- Design a modular Python ETL pipeline
- Transform semi-structured JSON data into relational tables
- Create a Star Schema data model
- Build an optimized Power BI model
- Develop an interactive dashboard for business users

---

## Technologies

- Python
- Pandas
- NumPy
- Power BI
- DAX
- Git
- GitHub

---

## Project Structure

```text
Tech-Sales-Analytics/
│
├── README.md
├── Documentation.md
├── main.py
├── config.py
│
├── src/
│   ├── extractor.py
│   ├── transformer.py
│   ├── dimensions.py
│   ├── fact.py
│   ├── validation.py
│   └── loader.py
│
├── data/
│   ├── input/
│   └── output/
│
├── powerbi/
│   ├── TechSalesDashboard.pbix
│   ├── Dashboard.png
│   └── DataModel.png
│
└── requirements.txt
```

#### Note
The original Sales.json (172 MB) is not included due to GitHub's file size limit.

A representative sample has been included for testing.

The ETL pipeline works without modification when the full dataset is placed in the Inputs folder.

---

## Dashboard Features

The dashboard includes:

- Executive KPI Cards
- Monthly Sales Trend
- Sales Comparison (2008 vs 2009)
- Forecast vs Actual
- Top 10 Products
- Product Sales Share
- Top Customer Analysis
- Country & State Filters
- Reset Dashboard button

---

## Dashboard Preview

![Dashboard](PowerBI/Dashboard.png)

---

## Data Model

![Data Model](PowerBI/Data%20Model.png)

---

## Business Insights

• 2009 sales declined by 15.4% compared to 2008.

• The United States generated the highest revenue.

• Refrigerator and Washer categories dominate sales.

• Forecast values exceed actual sales in all countries.

• Customer CS623 is the highest-value customer.

---

## Running the Project

Install dependencies

```bash
pip install -r requirements.txt
```

Run the ETL

```bash
python main.py
```

Load the generated CSV files into Power BI and open the provided `.pbix` file.

---

## Deliverables

- Python ETL Pipeline
- Structured CSV Output Files
- Star Schema Data Model
- Power BI Dashboard
- Technical Documentation

---
