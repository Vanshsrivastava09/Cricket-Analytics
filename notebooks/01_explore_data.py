# pandas is a library that lets us work with data like a spreadsheet
import pandas as pd

# pd.read_csv() reads a CSV file and turns it into a "dataframe"
# A dataframe is just a table with rows and columns — like Excel
matches = pd.read_csv('data/matches.csv')
deliveries = pd.read_csv('data/deliveries.csv')

# len() gives us the number of rows
print("=== MATCHES DATA ===")
print(f"Total matches: {len(matches)}")
print(f"Columns: {list(matches.columns)}")
print()
print(matches.head())  # .head() shows first 5 rows

print("\n=== DELIVERIES DATA ===")
print(f"Total deliveries: {len(deliveries)}")
print(f"Columns: {list(deliveries.columns)}")
print()
print(deliveries.head())