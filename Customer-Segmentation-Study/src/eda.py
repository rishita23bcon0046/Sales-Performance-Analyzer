import pandas as pd

# Load customer segmentation data
input_file = "data/processed/customer_segments.csv"

df = pd.read_csv(input_file)

print("Customer segmentation data loaded successfully!")
print(f"Number of customers: {len(df)}")

# Show the first 5 customers
print("\nFirst 5 customers:")
print(df.head())
# Count customers in each segment
segment_counts = df["Segment"].value_counts()

print("\nCustomers in each segment:")
print(segment_counts)
# Calculate average spending for each segment
average_spending = df.groupby("Segment")["Monetary"].mean().sort_values(ascending=False)

print("\nAverage spending by segment:")
print(average_spending)
import matplotlib.pyplot as plt

# Create a bar chart of customer segments
segment_counts.plot(kind="bar")
plt.title("Number of Customers by Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Number of Customers")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("data/processed/customer_segment_count.png")
plt.close()

plt.title("Number of Customers by Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Number of Customers")
plt.xticks(rotation=45)
plt.tight_layout()
# Create a bar chart of average spending by segment
average_spending.plot(kind="bar")

plt.title("Average Spending by Customer Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Average Spending")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("data/processed/average_spending_by_segment.png")
plt.close()