import pandas as pd
import random

# Load the CSV file
data = pd.read_csv('../data/data.csv')

# Calculate 10% of the rows
num_rows = len(data)
test_size = int(num_rows * 0.1)

# Randomly select 10% of the rows
test_indices = random.sample(range(num_rows), test_size)

# Split the data into train and test sets
test_data = data.iloc[test_indices]
train_data = data.drop(test_indices)

# Write the train data to a new file
train_data.to_csv('../data/train.csv', index=False)

# Write the test data to a new file
test_data.to_csv('../data/test.csv', index=False)