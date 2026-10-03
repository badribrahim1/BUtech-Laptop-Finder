import pandas as pd

# Read dataset
df = pd.read_excel("../data/laptops.xlsx")

# Show first 5 rows
print(df.head())

# Show dataset information
print("\nDataset shape:")
print(df.shape)

print("\nColumns:")
print(df.columns)

print("\nMissing values:")
print(df.isnull().sum())