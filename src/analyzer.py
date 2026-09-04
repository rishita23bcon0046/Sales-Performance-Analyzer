import pandas as pd

# Load cleaned sales data
data = pd.read_csv("data/processed/sales_data_clean.csv")

# Total Net Revenue
total_revenue = data["Net_Revenue"].sum()

# Total Profit
total_profit = data["Profit"].sum()

# Average Order Value
number_of_orders = data["Order_ID"].nunique()
aov = total_revenue / number_of_orders

# Total Units Sold
total_units = data["Quantity"].sum()

# Overall Profit Margin
profit_margin = (total_profit / total_revenue) * 100

# Revenue by Product
product_revenue = (
    data.groupby("Product")["Net_Revenue"]
    .sum()
    .sort_values(ascending=False)
)

# Profit by Product
product_profit = (
    data.groupby("Product")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

# Revenue by Region
region_revenue = (
    data.groupby("Region")["Net_Revenue"]
    .sum()
    .sort_values(ascending=False)
)

# Monthly Revenue
monthly_revenue = (
    data.groupby("Year_Month")["Net_Revenue"]
    .sum()
)

# Monthly Profit
monthly_profit = (
    data.groupby("Year_Month")["Profit"]
    .sum()
)

# Display results
print("===== SALES PERFORMANCE ANALYZER =====")

print("\nTotal Revenue:", round(total_revenue, 2))
print("Total Profit:", round(total_profit, 2))
print("Profit Margin:", round(profit_margin, 2), "%")
print("Average Order Value:", round(aov, 2))
print("Total Units Sold:", total_units)

print("\n===== REVENUE BY PRODUCT =====")
print(product_revenue)

print("\n===== PROFIT BY PRODUCT =====")
print(product_profit)

print("\n===== REVENUE BY REGION =====")
print(region_revenue)

print("\n===== MONTHLY REVENUE =====")
print(monthly_revenue)

print("\n===== MONTHLY PROFIT =====")
print(monthly_profit)
# Revenue by Customer
data = data[data["Customer_ID"] != "UNKNOWN"]
customer_revenue = (
    data.groupby("Customer_ID")["Net_Revenue"]
    
    .sum()
    .sort_values(ascending=False)
)

print("\n===== TOP 10 CUSTOMERS =====")
print(customer_revenue.head(10))
# Customer Segmentation
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

print("\n===== CUSTOMER SEGMENTS =====")
print(customer_segments.value_counts())