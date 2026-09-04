import pandas as pd
import numpy as np
from datetime import datetime, timedelta
start_date = datetime(2024, 1, 1)
num_orders = 5000
np.random.seed(42)
products = ["Laptop", "Printer", "Monitor", "Keyboard", "Mouse"]
categories = ["Electronics", "Office", "Accessories"]
customers = [f"CUST_{i:04d}" for i in range(1, 501)]
regions = ["North", "South", "East", "West"]
prices = {
    "Laptop": 60000,
    "Printer": 15000,
    "Monitor": 20000,
    "Keyboard": 2000,
    "Mouse": 800
}
order_ids = [f"ORD_{i:05d}" for i in range(1, num_orders + 1)]
dates = [start_date + timedelta(days=np.random.randint(0, 730)) for _ in range(num_orders)]
quantities = np.random.randint(1, 10, size=num_orders)
selected_products = np.random.choice(products, size=num_orders)
selected_customers = np.random.choice(customers, size=num_orders)
selected_regions = np.random.choice(regions, size=num_orders)
unit_prices = np.array([prices[p] for p in selected_products])
discounts = np.random.choice([0, 0.05, 0.10, 0.15, 0.20], size=num_orders)
data = pd.DataFrame({
        "Order_ID": order_ids,
            "Order_Date": dates,
                "Customer_ID": selected_customers,
                    "Product": selected_products,
                        "Category": np.random.choice(categories, size=num_orders),
                            "Region": selected_regions,
                                "Quantity": quantities,
                                    "Unit_Price": unit_prices,
                                        "Discount": discounts
                                        })

# Add dirty data
data.loc[10, "Region"] = np.nan
data.loc[20, "Quantity"] = 9999
data.loc[30, "Unit_Price"] = -500
data.loc[40, "Customer_ID"] = np.nan
data.loc[50, "Discount"] = np.nan
data.to_csv("data/raw/sales_data_raw.csv", index=False)
