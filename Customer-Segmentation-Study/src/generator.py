import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Make results reproducible
np.random.seed(42)
random.seed(42)

# Number of transactions
num_transactions = 5000

# Customer IDs
customer_ids = [f"C{str(i).zfill(4)}" for i in range(1, 1001)]

# Other data
genders = ["Male", "Female"]
cities = ["Jaipur", "Delhi", "Mumbai", "Pune", "Bangalore", "Kolkata"]
products = ["Laptop", "Monitor", "Keyboard", "Mouse", "Printer"]

# Product prices
product_prices = {
    "Laptop": 55000,
    "Monitor": 15000,
    "Keyboard": 1500,
    "Mouse": 800,
    "Printer": 12000
}

# Start date
start_date = datetime(2024, 1, 1)

data = []

for i in range(num_transactions):

    customer_id = random.choice(customer_ids)
    gender = random.choice(genders)
    age = random.randint(18, 60)
    city = random.choice(cities)
    product = random.choice(products)

    quantity = random.randint(1, 5)

    unit_price = product_prices[product]

    order_date = start_date + timedelta(
        days=random.randint(0, 730)
    )

    data.append([
        customer_id,
        gender,
        age,
        city,
        order_date,
        product,
        quantity,
        unit_price
    ])

# Create DataFrame
df = pd.DataFrame(data, columns=[
    "Customer_ID",
    "Gender",
    "Age",
    "City",
    "Order_Date",
    "Product",
    "Quantity",
    "Unit_Price"
])

# Add Revenue
df["Revenue"] = df["Quantity"] * df["Unit_Price"]

# Introduce some dirty data
df.loc[10, "Quantity"] = 9999
df.loc[25, "City"] = None
df.loc[40, "Customer_ID"] = None
df.loc[55, "Unit_Price"] = -500
df.loc[70, "City"] = " Jaipur "

# Save raw data
df.to_csv("data/raw/customer_data_raw.csv", index=False)

print("Customer dataset generated successfully!")
print(f"Total transactions: {len(df)}")
print("File saved to data/raw/customer_data_raw.csv")