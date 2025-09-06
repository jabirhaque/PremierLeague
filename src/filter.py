import pandas as pd

# Open the CSV file
input_file = '../data/2024:25.csv'
output_file = '../data/filtered_2024:25.csv'

# Load the data
data = pd.read_csv(input_file)

# Keep only the specified columns
columns_to_keep = ['Date','Time','HomeTeam','AwayTeam','FTR']
filtered_data = data[columns_to_keep]

# Save the filtered data to a new CSV file
filtered_data.to_csv(output_file, index=False)

print(f"Filtered data saved to {output_file}")