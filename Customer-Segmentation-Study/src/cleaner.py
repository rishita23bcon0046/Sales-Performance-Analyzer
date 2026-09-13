import pandas as pd

# Load raw data
input_file = "data/raw/customer_data_raw.csv"
output_file = "data/processed/customer_data_clean.csv"

df = pd.read_csv(input_file)

print("Raw data loaded successfully!")
print(f"Rows before cleaning: {len(df)}")

# Remove duplicate rows
df = df.drop_duplicates()

# Standardize text columns
df["Customer_ID"] = df["Customer_ID"].astype("string").str.strip()
df["City"] = df["City"].astype("string").str.strip()
df["Gender"] = df["Gender"].astype("string").str.strip()
df["Product"] = df["Product"].astype("string").str.strip()

# Convert date column
df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")

# Remove invalid quantities
df.loc[(df["Quantity"] <= 0) | (df["Quantity"] > 100), "Quantity"] = pd.NA
# Remove rows with missing important values
df = df.dropna(subset=["Customer_ID", "Order_Date", "Quantity", "Unit_Price"])

# Save cleaned data
output_file = "data/processed/customer_data_clean.csv"
df.to_csv(output_file, index=False)

print("Cleaning completed successfully!")
print(f"Rows after cleaning: {len(df)}")
print(f"Cleaned file saved to: {output_file}")
