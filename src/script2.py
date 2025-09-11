import pandas as pd

# List of CSV files to merge
csv_files = ['../data/2026.csv', '../data/2025.csv', '../data/2024.csv',
             '../data/2023.csv', '../data/2022.csv', '../data/2021.csv', '../data/2020.csv']

# Initialize an empty DataFrame
merged_data = pd.DataFrame()

# Loop through each file and append its data
for file in csv_files:
    data = pd.read_csv(file)
    merged_data = pd.concat([merged_data, data], ignore_index=True)

# Write the merged data to a new CSV file
merged_data.to_csv('../data/data.csv', index=False)