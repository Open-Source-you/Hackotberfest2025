# author: seema kumari patel
# Implementation of data extraction and plotting using pandas and matplotlib

import matplotlib.pyplot as plt
import pandas as pd

# Read the CSV file
df = pd.read_csv("data.csv")

# Display first few rows
print(df.head())

# Plot sales trends
plt.figure(figsize=(10, 6))
plt.plot(df["Month"], df["Product_A"], marker="o", label="Product A")
plt.plot(df["Month"], df["Product_B"], marker="s", label="Product B")

plt.title("Monthly Sales Data")
plt.xlabel("Month")
plt.ylabel("Units Sold")
plt.legend()
plt.grid(True)
plt.show()
