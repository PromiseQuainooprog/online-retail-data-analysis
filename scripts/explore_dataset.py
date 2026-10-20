# Import pandas for data analysis
import pandas as pd 

# Load the original dataset
raw_data = pd.read_csv("raw\OnlineRetail.csv")

# Display the first five rows
print("First five rows:", raw_data.head())

# Display the number of rows and columns
print("Dataset Shape:", raw_data.shape)

#print("Number of rows:",raw_data.shape[0])

#print("Number of columns:",raw_data.shape[1])

# Display the columns name
print("Column names:", raw_data.columns.tolist())

# Display column data type
print("Data Column Type:",raw_data.dtypes)

# Display dataset information
print("Dataset Information:",raw_data.info)

# Count missing values in each column
print("Missing Values:",raw_data.isnull().sum())

# Count duplicate rows
print("Duplicate Rows:",raw_data.duplicated().sum())