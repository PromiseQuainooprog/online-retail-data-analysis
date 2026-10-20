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
   # connection.close()
else:
    print("ERROE: Cleaned dataset not found.Check file location")

# Check the total number of rows using SQL
cursor = connection.cursor()

cursor.execute("""
     SELECT COUNT(*)
     FROM OnlineRetail
""")

total_rows = cursor.fetchone()[0]

print("Total rows verified using SQL:", total_rows)

# Check missing values using SQL
cursor.execute("""
    SELECT
        SUM(CASE WHEN Description IS NULL THEN 1 ELSE 0 END)
            AS Missing_Descriptions,
        SUM(CASE WHEN CustomerID IS NULL THEN 1 ELSE 0 END)
            AS MissingCustomerIDs,
        SUM(CASE WHEN InvoiceDate IS NULL THEN 1 ELSE 0 END)
            AS Missing_InvoiceDates,
        SUM(CASE WHEN Quantity IS NULL THEN 1 ELSE 0 END) 
            AS Missing_Quantities,
        SUM(CASE WHEN UnitPrice IS NULL THEN 1 ELSE 0 END)
            AS Missing_UnitPrices
     FROM OnlineRetail
""")
missing_values = cursor.fetchone()

print(" ================= Missing Values Check =============== ")
print("Missing descriptions:", missing_values[0])
print("Missing customer IDs:", missing_values[1])
print("Missing invoice dates:", missing_values[2])
print("Missing quantities:", missing_values[3])
print("Missing nit prices:", missing_values[4])

#  Check Positive, Negative, and Zero Quantities
cursor.execute("""
     SELECT
        SUM(CASE WHEN Quantity > 0 THEN 1 ELSE 0 END)
            AS Positive_Quantity_Rows,
        SUM(CASE WHEN Quantity < 0 THEN 1 ELSE 0 END)
            AS Negative_Quantity_Rows,
        SUM(CASE WHEN Quantity = 0 THEN 1 ELSE 0 END)
            AS Zero_Quantity_Rows
    FROM OnlineRetail        
""")
quantity_results = cursor.fetchone()

print("=============== QUANTITY VALIDATION ===========")
print("Positive quantity rows:", quantity_results[0])
print("Negative quantity rows:", quantity_results[1])
print("Zero quantity rows:", quantity_results[2])

# Validate sales values using SQL
cursor.execute("""
    SELECT
        SUM(CASE WHEN Quantity * UnitPrice > 0 THEN Quantity * UnitPrice ELSE 0 END)
            AS Positive_Sales,
        SUM(CASE WHEN Quantity * UnitPrice < 0 THEN Quantity * UnitPrice ELSE 0 END)
            AS Negative_Sales,
        SUM(Quantity * UnitPrice) AS Net_Sales
    FROM OnlineRetail       
""")

sales_results = cursor.fetchone()

print("============== SALES VALIDATION =============")
print("Positive Sales:",round(sales_results[0], 2))
print("Negative Sales:",round(sales_results[1], 2))
print("Net Sales:",round(sales_results[2], 2))

# Validate Business Statistics Using SQL
cursor.execute("""
    SELECT
        COUNT(DISTINCT InvoiceNo),
        COUNT(DISTINCT CustomerID),
        COUNT(DISTINCT StockCode),
        COUNT(DISTINCT Country)
    FROM OnlineRetail    
""")

business_stats = cursor.fetchone()
print("================= BUSINESS STATISTICS ============")
print("Total Invooices:", business_stats[0])
print("Unique CustomerID:", business_stats[1])
print("Unique StockCode:", business_stats[2])
print("Total Countries:", business_stats[3])

# =========================
# TOP 10 CUSTOMERS BY NET SALES
# ==============================

cursor.execute("""
    SELECT
        CustomerID,
        ROUND(SUM(Quantity * UnitPrice), 2) AS NetSales
    FROM OnlineRetail    
    WHERE CustomerID IS NOT NULL
    GROUP BY CustomerID
    ORDER BY NetSales DESC
    LIMIT 10
""")

top_customers = cursor.fetchone()

print("=============== TOP 10 CUSTOMERS ================")
print("Customer ID | NetSales (£)")
print("-"*35)

for customer in top_customers:
    print(customer, "| £", f"{customer:,.2f}")

# ===============================
# TOP 10 PRODUCT BY NET SALES
# ===============================

cursor.execute("""
    SELECT
       StockCode,
       Description,
       ROUND(SUM(Quantity * UnitPrice), 2) AS NETSALES
    FROM OnlineRetail
    GROUP BY StockCode, Description
    ORDER BY NetSales DESC
    LIMIT 10           
""")

top_products = cursor.fetchall()

print("=================== TOP 10 PRODUCTS ================")
print("Product Code | Description | Net Sales (£)")
print("-"*75)

for product in top_products:
    print(
        product[0], "|",
        product[1],"| £",
        f"{product[2]:,.2f}"
    )

# ============================
# TOP 10 COUNTRIES
# ===========================

cursor.execute("""
    SELECT
        Country,
        ROUND(SUM(Quantity * UnitPrice), 2) AS NetSales
    FROM OnlineRetail
    GROUP BY Country
    ORDER BY NetSales DESC
    LIMIT 10
""")

top_countries = cursor.fetchall()

print("============== TOP 10 COUNTRIES ==============")
print("Country | NetSales (£)")
print("-"*45)

for country in top_countries:
    print(country[0], "| £", f"{country[1]:,.2f}")

# =======================
# MONTHLY SALES ANALYSIS
# =======================
cursor.execute("""
    SELECT
       strftime('%Y-%m', InvoiceDate) AS YearMonth,
       ROUND(SUM(Quantity * UnitPrice), 2) AS NetSales
    FROM OnlineRetail
    GROUP BY YearMonth
    ORDER BY YearMonth
""")

monthly_sales = cursor.fetchall()

print("============ MONTHLY SALES ANALYSIS ============")
print("Month | NetSales (£)")
print("-"*45)

for month in monthly_sales:
    print(f"{month[0]} | £{month[1]:,.2f}")

