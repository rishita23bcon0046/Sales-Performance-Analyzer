import pandas as pd
import numpy as np

# Load raw sales data
data = pd.read_csv("data/raw/sales_data_raw.csv")

# Data quality before cleaning
raw_rows = len(data)
missing_before = data.isnull().sum().sum()
quantity_outliers = (data["Quantity"] > 100).sum()
invalid_prices = (data["Unit_Price"] <= 0).sum()
# Convert Order_Date to proper date format
data["Order_Date"] = pd.to_datetime(data["Order_Date"], errors="coerce")

# Fill missing Region with the most common region
data["Region"] = data["Region"].fillna(data["Region"].mode()[0])

# Fill missing Customer_ID with "UNKNOWN"
data["Customer_ID"] = data["Customer_ID"].fillna("UNKNOWN")

# Fill missing Discount with 0
data["Discount"] = data["Discount"].fillna(0)

# Fix invalid Quantity values
median_quantity = data.loc[data["Quantity"] < 100, "Quantity"].median()
data.loc[data["Quantity"] > 100, "Quantity"] = median_quantity

# Fix negative Unit_Price values
median_price = data.loc[data["Unit_Price"] > 0, "Unit_Price"].median()
data.loc[data["Unit_Price"] <= 0, "Unit_Price"] = median_price

# Calculate Net Revenue
data["Net_Revenue"] = (
    data["Quantity"] * data["Unit_Price"] * (1 - data["Discount"])
)

# Assume Total Cost is 70% of Net Revenue
data["Total_Cost"] = data["Net_Revenue"] * 0.70

# Calculate Profit
data["Profit"] = data["Net_Revenue"] - data["Total_Cost"]

# Calculate Profit Margin
data["Profit_Margin"] = (
    data["Profit"] / data["Net_Revenue"]
) * 100

# Create Year-Month column
data["Year_Month"] = data["Order_Date"].dt.to_period("M").astype(str)

# Create Day Name column
data["Day_Name"] = data["Order_Date"].dt.day_name()

# Save cleaned data
data.to_csv("data/processed/sales_data_clean.csv", index=False)

print("Data cleaning completed successfully!")
print("Cleaned data saved to data/processed/sales_data_clean.csv")
print("Rows:", len(data))
print("Columns:", len(data.columns))