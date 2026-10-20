# Import the required libraries
import pandas as pd  
import sqlite3 
import os

# Get the location of the main project folder
project_folder = os.getcwd()

print("Main Project folder:", project_folder)

# Locate  the cleaned dataset
csv_path = os.path.join(project_folder,"..", "data","processed","CleanedOnlineRetail.csv")

# Locate the database we will create
database_path = os.path.join(project_folder,"..","data","processed","Online_Retail.db")

# Display the file location
print("Project Folder:", project_folder)
print("Cleaned dataset:", csv_path)
print("Database location:", database_path)

# Check whether the cleaned dataset exist
if os.path.exists(csv_path):
    print("Success: Cleaned dataset found!")

    # Load the cleaned dataset
    sql_data = pd.read_csv(csv_path, encoding="ISO-8859-1")

    # Connect to SQLite
    connection = sqlite3.connect(database_path)

    # Save the data into a database table
    sql_data.to_sql("OnlineRetail", connection, if_exists="replace", index=False)

    # Display comfirmation
    print("Cleaned data successfully loaded into SQLite!")
    print("Total rows:", len(sql_data))

    # Close the connection
    connection.close()
else:
    print("ERROE: Cleaned dataset not found.Check file location")
