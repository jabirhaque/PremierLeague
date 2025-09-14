import pandas as pd
import random

data = pd.read_csv('../data/data.csv')
num_rows = len(data)
test_size = int(num_rows * 0.1)
test_indices = random.sample(range(num_rows), test_size)
test_data = data.iloc[test_indices]
train_data = data.drop(test_indices)
train_data.to_csv('../data/train.csv', index=False)
test_data.to_csv('../data/test.csv', index=False)