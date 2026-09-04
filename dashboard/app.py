import streamlit as st
import pandas as pd

# Page settings
st.set_page_config(
    page_title="Sales Performance Analyzer",
    page_icon="📊",
    layout="wide"
)

# Load cleaned data
data = pd.read_csv("data/processed/sales_data_clean.csv")
# Data Cleaning Audit
raw_data = pd.read_csv("data/raw/sales_data_raw.csv")
clean_data = pd.read_csv("data/processed/sales_data_clean.csv")

st.subheader("🧹 Data Cleaning Audit")

raw_rows = len(raw_data)
clean_rows = len(clean_data)

missing_before = raw_data.isnull().sum().sum()
missing_after = clean_data.isnull().sum().sum()

quantity_outliers = (raw_data["Quantity"] > 100).sum()
invalid_prices = (raw_data["Unit_Price"] <= 0).sum()

preservation_rate = (clean_rows / raw_rows) * 100

col1, col2, col3 = st.columns(3)

col1.metric("Raw Rows", f"{raw_rows:,}")
col2.metric("Clean Rows", f"{clean_rows:,}")
col3.metric("Data Preserved", f"{preservation_rate:.1f}%")

col4, col5, col6 = st.columns(3)

col4.metric("Missing Values Before", f"{missing_before:,}")
col5.metric("Missing Values After", f"{missing_after:,}")
col6.metric("Quantity Outliers", f"{quantity_outliers:,}")

st.write("### Cleaning Issues Detected")

audit_data = pd.DataFrame({
    "Issue": [
        "Missing Values",
        "Quantity Outliers",
        "Invalid Prices"
    ],
    "Before Cleaning": [
        missing_before,
        quantity_outliers,
        invalid_prices
    ],
    "After Cleaning": [
        missing_after,
        0,
        0
    ]
})

st.dataframe(audit_data, use_container_width=True)
# Convert Order_Date to datetime
data["Order_Date"] = pd.to_datetime(data["Order_Date"])

# Date range filter
start_date = data["Order_Date"].min().date()
end_date = data["Order_Date"].max().date()

selected_dates = st.sidebar.date_input(
    "Select Date Range",
    value=(start_date, end_date),
    min_value=start_date,
    max_value=end_date
)

# Apply date filter
if len(selected_dates) == 2:
    data = data[
        (data["Order_Date"].dt.date >= selected_dates[0]) &
        (data["Order_Date"].dt.date <= selected_dates[1])
    ]

# Region filter
selected_region = st.sidebar.selectbox(
    "Select Region",
    ["All"] + sorted(data["Region"].dropna().unique().tolist())
)

# Apply region filter
if selected_region != "All":
    data = data[data["Region"] == selected_region]

# Product filter
selected_product = st.sidebar.selectbox(
    "Select Product",
    ["All"] + sorted(data["Product"].unique().tolist())
)



# Apply product filter
if selected_product != "All":
    data = data[data["Product"] == selected_product]

# Title
st.title("📊 Sales Performance Analyzer")

st.write("Interactive dashboard for analyzing sales performance.")

# KPI calculations
total_revenue = data["Net_Revenue"].sum()
total_profit = data["Profit"].sum()
profit_margin = (total_profit / total_revenue) * 100
total_orders = data["Order_ID"].nunique()
total_units = data["Quantity"].sum()
aov = total_revenue / total_orders

# KPI cards
col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
col2.metric("Total Profit", f"₹{total_profit:,.0f}")
col3.metric("Profit Margin", f"{profit_margin:.1f}%")
col4.metric("Total Orders", f"{total_orders:,}")
col5.metric("Units Sold", f"{total_units:,}")
col6.metric("Average Order Value", f"₹{aov:,.0f}")

# Revenue by product
st.subheader("Revenue by Product")

product_revenue = (
    data.groupby("Product")["Net_Revenue"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(product_revenue)
# Profit by Product
st.subheader("Profit by Product")

product_profit = (
    data.groupby("Product")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(product_profit)

# Revenue by region
st.subheader("Revenue by Region")

region_revenue = (
    data.groupby("Region")["Net_Revenue"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(region_revenue)

# Monthly revenue
st.subheader("Monthly Revenue")

monthly_revenue = (
    data.groupby("Year_Month")["Net_Revenue"]
    .sum()
)

st.line_chart(monthly_revenue)

# Monthly profit
st.subheader("Monthly Profit")

monthly_profit = (
    data.groupby("Year_Month")["Profit"]
    .sum()
)

st.line_chart(monthly_profit)
# Customer Segmentation
st.subheader("Customer Segmentation")

customer_revenue = (
    data[data["Customer_ID"] != "UNKNOWN"]
    .groupby("Customer_ID")["Net_Revenue"]
    .sum()
)

def customer_segment(revenue):
    if revenue >= 1000000:
        return "Platinum"
    elif revenue >= 500000:
        return "Gold"
    elif revenue >= 200000:
        return "Silver"
    else:
        return "Bronze"

customer_segments = customer_revenue.apply(customer_segment)

segment_counts = customer_segments.value_counts()

st.bar_chart(segment_counts)
# Top 10 Customers
st.subheader("Top 10 Customers")

top_customers = (
    data.groupby("Customer_ID")["Net_Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_customers)
# Discount Analysis
st.subheader("Discount Analysis")

discount_analysis = (
    data.groupby("Discount")[["Net_Revenue", "Profit"]]
    .sum()
    .reset_index()
)

discount_analysis["Discount"] = (
    discount_analysis["Discount"] * 100
).astype(int).astype(str) + "%"

st.write("Revenue and Profit by Discount Level")

st.dataframe(discount_analysis)

st.bar_chart(
    discount_analysis.set_index("Discount")[["Net_Revenue", "Profit"]]
)
# Monthly Sales Trend
st.subheader("Monthly Sales Trend")

monthly_sales = (
    data.groupby("Year_Month")["Net_Revenue"]
    .sum()
    .reset_index()
)

st.line_chart(
    monthly_sales.set_index("Year_Month")["Net_Revenue"]
)

# Month-over-Month Growth
monthly_sales["MoM_Growth"] = (
    monthly_sales["Net_Revenue"].pct_change() * 100
)

st.subheader("Month-over-Month Growth")

st.dataframe(
    monthly_sales
)
# Product Insights
st.subheader("📦 Product Insights")

product_analysis = (
    data.groupby("Product")
    .agg(
        Revenue=("Net_Revenue", "sum"),
        Profit=("Profit", "sum"),
        Units_Sold=("Quantity", "sum")
    )
    .sort_values("Revenue", ascending=False)
)

st.write("### Product Performance")

st.dataframe(
    product_analysis,
    use_container_width=True
)

st.write("### Revenue by Product")

st.bar_chart(
    product_analysis["Revenue"]
)

st.write("### Profit by Product")

st.bar_chart(
    product_analysis["Profit"]
)
# Product Insights
st.subheader("📦 Product Insights")

product_analysis = (
    data.groupby("Product")
    .agg(
        Revenue=("Net_Revenue", "sum"),
        Profit=("Profit", "sum"),
        Units_Sold=("Quantity", "sum")
    )
    .sort_values("Revenue", ascending=False)
)

st.write("### Product Performance")

st.dataframe(
    product_analysis,
    use_container_width=True
)

st.write("### Revenue by Product")

st.bar_chart(
    product_analysis["Revenue"]
)

st.write("### Profit by Product")

st.bar_chart(
    product_analysis["Profit"]
)
# Business Insights
st.subheader("💡 Business Insights")

# Best Product
best_product = (
    data.groupby("Product")["Net_Revenue"]
    .sum()
    .idxmax()
)

best_product_revenue = (
    data.groupby("Product")["Net_Revenue"]
    .sum()
    .max()
)

# Best Region
best_region = (
    data.groupby("Region")["Net_Revenue"]
    .sum()
    .idxmax()
)

best_region_revenue = (
    data.groupby("Region")["Net_Revenue"]
    .sum()
    .max()
)

# Top Customer
top_customer = (
    data.groupby("Customer_ID")["Net_Revenue"]
    .sum()
    .idxmax()
)

top_customer_revenue = (
    data.groupby("Customer_ID")["Net_Revenue"]
    .sum()
    .max()
)

# Best Month
best_month = (
    data.groupby("Year_Month")["Net_Revenue"]
    .sum()
    .idxmax()
)

# Average Discount
average_discount = data["Discount"].mean() * 100

col1, col2, col3 = st.columns(3)

col1.metric(
    "🏆 Best Product",
    best_product
)

col2.metric(
    "🌍 Best Region",
    best_region
)

col3.metric(
    "👑 Top Customer",
    top_customer
)

st.write("### Key Findings")

st.write(
    f"🏆 **{best_product}** generated the highest revenue of "
    f"₹{best_product_revenue:,.0f}."
)

st.write(
    f"🌍 **{best_region}** was the highest-performing region with "
    f"₹{best_region_revenue:,.0f} in revenue."
)

st.write(
    f"👑 **{top_customer}** generated the highest customer revenue of "
    f"₹{top_customer_revenue:,.0f}."
)

st.write(
    f"📅 **{best_month}** was the best month based on revenue."
)

st.write(
    f"🎯 The average discount given was **{average_discount:.1f}%**."
)