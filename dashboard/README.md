# 📊 Sales Performance Analyzer

An end-to-end sales analytics project that cleans, analyzes, and visualizes sales data to generate useful business insights.

## 🎯 Project Objective

The main objective of this project is to analyze sales data and help a business understand:

- Total revenue and profit
- Best-performing products
- Best-performing regions
- Monthly sales trends
- Customer segments
- Discount performance
- Month-over-month growth
- Data quality issues

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Streamlit
- Plotly
- Excel
- Power BI

## 🔄 Project Workflow

Raw Sales Data
        ↓
Data Generation
        ↓
Data Cleaning
        ↓
Data Analysis
        ↓
KPI Calculation
        ↓
Streamlit Dashboard
        ↓
Business Insights

## 🧹 Data Cleaning

The project intentionally contains dirty data to simulate a real-world business dataset.

Examples include:

- Missing values
- Invalid quantities
- Negative prices
- Missing customer IDs
- Missing discounts

The Python cleaning process fixes these issues and creates a clean dataset for analysis.

## 📈 Key KPIs

The dashboard tracks:

- Total Revenue
- Total Profit
- Profit Margin
- Total Orders
- Units Sold
- Average Order Value

## 👥 Customer Analytics

Customers are segmented into:

- Platinum
- Gold
- Silver
- Bronze

This helps identify high-value customers.

## 📦 Product Analysis

The project analyzes product-level:

- Revenue
- Profit
- Units Sold

## 🌍 Regional Analysis

Sales performance is analyzed across:

- North
- South
- East
- West

## 📊 Dashboard

The Streamlit dashboard provides:

- Sales overview
- Data cleaning audit
- Product insights
- Customer analytics
- Discount analysis
- Monthly sales trends
- Month-over-month growth
- Business insights

## 📁 Project Structure

```text
Sales-Performance-Analyzer/
│
├── data/
│   ├── raw/
│   │   └── sales_data_raw.csv
│   │
│   └── processed/
│       └── sales_data_clean.csv
│
├── src/
│   ├── generator.py
│   ├── cleaner.py
│   └── analyzer.py
│
├── dashboard/
│   └── app.py
│
├── requirements.txt
└── README.md