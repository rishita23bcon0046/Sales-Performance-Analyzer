import pandas as pd

# Load cleaned data
input_file = "data/processed/customer_data_clean.csv"

df = pd.read_csv(input_file)

print("Cleaned data loaded successfully!")
print(f"Rows available: {len(df)}")
# Calculate revenue for each transaction
df["Revenue"] = df["Quantity"] * df["Unit_Price"]

print("Revenue calculated successfully!")
# Convert Order_Date to datetime
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# Set the analysis date as one day after the latest order
analysis_date = df["Order_Date"].max() + pd.Timedelta(days=1)

# Calculate RFM values for each customer
rfm = df.groupby("Customer_ID").agg(
    Recency=("Order_Date", lambda x: (analysis_date - x.max()).days),
    Frequency=("Order_Date", "count"),
    Monetary=("Revenue", "sum")
).reset_index()

print("RFM analysis completed successfully!")
print(f"Number of customers analyzed: {len(rfm)}")
# Create RFM scores from 1 to 5

# Recency: lower is better
rfm["R_Score"] = pd.qcut(
    rfm["Recency"],
    5,
    labels=[5, 4, 3, 2, 1]
)

# Frequency: higher is better
rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
)

# Monetary: higher is better
rfm["M_Score"] = pd.qcut(
    rfm["Monetary"],
    5,
    labels=[1, 2, 3, 4, 5]
)

print("RFM scores created successfully!")
# Convert RFM scores to numbers
rfm["R_Score"] = rfm["R_Score"].astype(int)
rfm["F_Score"] = rfm["F_Score"].astype(int)
rfm["M_Score"] = rfm["M_Score"].astype(int)

# Calculate overall RFM score
rfm["RFM_Score"] = (
    rfm["R_Score"]
    + rfm["F_Score"]
    + rfm["M_Score"]
)

print("Overall RFM score calculated successfully!")
# Create customer segments
def segment_customer(score):
    if score >= 13:
        return "Champions"
    elif score >= 10:
        return "Loyal Customers"
    elif score >= 7:
        return "Potential Loyalists"
    elif score >= 5:
        return "At Risk"
    else:
        return "Lost Customers"


rfm["Segment"] = rfm["RFM_Score"].apply(segment_customer)

print("Customer segmentation completed successfully!")
print(rfm[["Customer_ID", "RFM_Score", "Segment"]].head(10))
# Save final customer segmentation data
output_file = "data/processed/customer_segments.csv"

rfm.to_csv(output_file, index=False)

print("Customer segmentation data saved successfully!")
print(f"File saved to: {output_file}")