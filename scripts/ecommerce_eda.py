# =================================
# ANALYSTLAB AFRICA INTERSHIP
# WEEK 1-2: EXPLORATORY DATA ANALYSIS
# Dataset: Online Retail 
# =====================================

# Import the required libraries
import pandas as pd   
import numpy as np  
import matplotlib.pyplot as plt     

# ---------------------------------------
# 1. Load the Cleaned dataset
# ------------------------------------

explore_data = pd.read_csv("../data/processed/Cleaned_OnlineRetail.csv")

print("Dataset shape:", explore_data.shape)

# ------------------------------
# 2. Inspect the Data
# --------------------------

print("First five rows:", explore_data.head())

print("Column names:", explore_data.columns.tolist())

print("Data tpye:", explore_data.dtypes)

# --------------------------
# 3. Summary Statistics
# ---------------------------

print("Numerical Summary:", explore_data.describe())

print("Number of unique products:", explore_data["StockCode"].unique())

print("Number of country:", explore_data["Country"].unique())

print("Number of unique customers:", explore_data["CustomerID"].unique())

# ----------------------------------
# 4. Prepare Date and Time Variables
# ------------------------------------

explore_data["InvoiceDate"] = pd.to_datetime(explore_data["InvoiceDate"])

explore_data["YearMonth"] = explore_data["InvoiceDate"].dt.to_period("M")

# -----------------------------------
# 5. Inspect Inovice Numbers
# ----------------------------------

explore_data["InvoiceNo"] = explore_data["InvoiceNo"].astype(str).str.strip()

# In the dataset, invoice numbers beginning with C commonly indicate cancelations.

explore_data["IsCancellation"] = explore_data["InvoiceNo"].str.upper().str.startswith("C")

print("Cancellation records:", explore_data["IsCancellation"].value_counts())

print("Negative quantity records:", (explore_data["Quantity"]<0).sum())

# --------------------------
# 6. Calculate Sales Value
# --------------------------

# Calculate the sales value of each transacttion line
explore_data["SaleValue"] = explore_data["Quantity"] * explore_data["UnitPrice"]

# Display the first five calculated sales value
print("Sale Value:", (explore_data[["Quantity","UnitPrice","SaleValue"]].head()))

# Calculated total signed sales value
print("Total Signed Sales Value:", explore_data["SaleValue"].sum())


# -----------------------------------
# 7. Calculate Sales value By Country
# -----------------------------------

country_sales = (explore_data.groupby("Country")["SaleValue"].sum().sort_values(ascending=False))

top_country = explore_data.groupby("Country")["SaleValue"].sum().sort_values(ascending=True).head(10)

print("Top 10 countries by signed sales value:",country_sales.head(10))

# ---------------------------------------
# 8. Calculate Monthly Signed Sales Value
# ---------------------------------------

monthly_sales = (explore_data.groupby("YearMonth")["SaleValue"].sum())

print("Monthly signed sales value:",monthly_sales)

# -----------------------------------
# 9. Calculate Sales Value by Product
# ------------------------------------

product_sales = (explore_data.groupby("Description")["SaleValue"].sum().sort_values(ascending=False))
top_product = explore_data.groupby("Description")["SaleValue"].sum().sort_values(ascending=False).head(10)

print("Top 10 proudct by signed sales value:", product_sales.head(10))


# ===============================
# VISUALIZATION
# ==========================

# --------------------------------------
# 10. Chart 1: Monthly Sales Trend Chart
# --------------------------------------

# Convert monthly periods to strings for plotting 
monthly_sales.index = monthly_sales.index.astype(str)

plt.figure(figsize=(12, 6))
plt.plot(monthly_sales.index, monthly_sales.values,marker="o"
)
plt.title("Monthly Sales Value Trend")
plt.xlabel("Month")
plt.ylabel("Signed Sales Value")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig("Monthly Sales Value Trend.png")

# -------------------------------------------
# 11. Chart 2: Top 10 Products By Sales Value 
# -------------------------------------------

plt.figure(figsize=(12,7))
top_product.sort_values().plot(kind="bar")
plt.title("Top 10 Product By Signed Sales Value")
plt.xlabel("Product")
plt.ylabel("Signed Sales Value")
plt.tight_layout()
plt.savefig("Top 10 Product By Signed Sales Value.png")

# --------------------------------------------
# 12. Chart 3: Top 10 Countries by Sales Value
# --------------------------------------------
plt.figure(figsize=(12,6))
top_country.sort_values().plot(kind="barh")
plt.title("Top 10 Countries by Signed Sales Value")
plt.xlabel("Signed Sales Value")
plt.ylabel("Country")
plt.tight_layout()
plt.savefig("Top 10 Countries by Signed Sales Value.png")

# =================================
# STATISTICAL ANALYSIS
# =================================

print("============== STATISTICAL SUMMARY ===========")

# Total number of transactions (invoice)
total_invoices = explore_data["InvoiceNo"].nunique()
print("Total Invoices:", total_invoices)

# Total number of unique customers
total_customers = explore_data["CustomerID"].nunique()
print("Unique Customers:", total_customers)

# Total number of Products
total_products = explore_data["StockCode"].nunique()
print("Unique Product:", total_products)

# Total number of countries
total_countries = explore_data["Country"].nunique()
print("Countries:", total_countries)

# Total quantity sold (net of negativee quantities)
total_quantity = explore_data["Quantity"].sum()
print("Net Quantity:", total_quantity)

# Total Sales Value (net of negative quantities)
total_sales = explore_data["SaleValue"].sum()
print("Net Sales Value (£):",round(total_sales, 2))

# Average Unit Price
average_price = explore_data["UnitPrice"].mean()
print("Average Unit Price (£):",round(average_price, 2))

# Average invoice value
invoice_value = explore_data.groupby("InvoiceNo")["SaleValue"].sum()
average_invoice_value = invoice_value.mean()
print("Average Invoice VAlue (£):", round(average_invoice_value, 2))

# MissingValues
print("Missing Values:",explore_data.isnull().sum())

# =============================
# MISSING VALUES ANALYSIS
# =============================

print("=============== MISSING VALUES ANALYSIS ============")

# Count missing values
missing_values = explore_data.isnull().sum()

# Calculate missing peercentages
missing_percentage = (missing_values / len(explore_data)) * 100

# Create a summary table 
missing_summary = pd.DataFrame({
    "Missing Values": missing_values, 
    "Missing Percentage": missing_percentage.round(2)})

# Show columns that have missing values
missing_summary = missing_summary[missing_summary["Missing Values"] > 0]

print(missing_summary)

# ==========================
# CANCELLATION ANALYSIS
# =========================

print("============== CANCELLATION ANALYSIS ================")

# Count cancellation invoices
cancellations = explore_data["IsCancellation"].astype(str).str.strip().str.lower().isin(["true", "1", "yes"])

cancellation_rows = explore_data[cancellations]

print("Cancellation rows:", len(cancellation_rows))

print("Unique cancellation invoices:",cancellation_rows["InvoiceNo"].nunique())

# Count row iwth negative quantities
negative_quantity_rows = explore_data[explore_data["Quantity"] < 0]
print("Rows with negative quantities:", len(negative_quantity_rows))

# Calculate the value associated with negative quantities
print("Values of negative quantity rows (£):", round(negative_quantity_rows["SaleValue"].sum(), 2))

# Count rows with negative unit prices
negative_price_rows = explore_data[explore_data["UnitPrice"] < 0]

print("Rows with negative unit prices:", len(negative_price_rows))

# ====================================
# POSITIVE AND NEGATIVE SALES ANALYSIS
# ====================================

print("============== POSITIVE AND NEGATIVE ANALYSIS =============")

# Select rows with positive quantities
positive_sales = explore_data[explore_data["Quantity"] > 0]

# Select rows with negative quantities
negative_sales = explore_data[explore_data["Quantity"] < 0]

# Calculate positive sales values
positive_sales_values = positive_sales["SaleValue"].sum()

# Calculate negative sales values
negative_sales_values = negative_sales["SaleValue"].sum()

# Calculate Net Sales
net_sales_values = explore_data["SaleValue"].sum()

# Display the results
print("Positive sale values (£):", round(positive_sales_values, 2))

print("Negative sales values (£):", round(negative_sales_values, 2))

print("Net Sales Value (£):", round(net_sales_values, 2))

# Calculate the number of rows in each category
print("Positive quantity rows:", len(positive_sales))

print("Negative quantity rows:", len(negative_sales))

print("Zero quantity rows:", len(explore_data[explore_data["Quantity"] == 0]))

# Check for duplicate rows 
duplicate_count = explore_data.duplicated().sum()

print("Duplicate rows remaining:", duplicate_count)

# ==============================
# MONTHLY SALES GROWTH ANALYSIS
# ===============================

# Calculate total sales for each month
monthly_sales = (
    explore_data.groupby("YearMonth")["SaleValue"].sum().sort_index()
)

# Calculate the percentage chnage from the pervious month
monthly_growth = monthly_sales.pct_change() * 100

# Display the results 
print("========= MONTHLY SALES GROWTH ===========")
print("Month | NetSales (£) | Growth (%)")
print("-"*55)

for month in monthly_sales.index:
    sales = monthly_sales.loc[month]
    growth = monthly_growth.loc[month]

    if pd.isna(growth):
        print(f"{month} | £{sales:,.2f} | N/A")
    else:
        print(f"{month} | £{sales:,.2f} | {growth:+.2f}%")  

# ============================
# AVERAGE ORDER VALUE ANALYSIS
# ============================

# Exculde cancelled invoice
sales_data = explore_data[
    ~explore_data["InvoiceNo"].astype(str).str.startswith("C")
].copy()

# Calculate the total sales value for each invoice
invoice_totals = (
    sales_data.groupby("InvoiceNo")["SaleValue"].sum())

# Keep invoices with positive tottal values
invoice_totals = invoice_totals[invoice_totals > 0]

# Calculate the average order value
average_order_value = invoice_totals.mean()

# Display the results
print("=============== AVERAGE ORDER VALUE ============")
print("Average Order Value:",round(average_order_value, 2))
print("Number of Valid Invoices:", {len(invoice_totals)})

# ================================
# TOP 10 HIGHEST-VALUE INVOICES
# ==============================

# Start invoice totals from highest to lowest
top_invoice = invoice_totals.sort_values(
    ascending=False
).head(10)

# Display the results
print("========= TOP 10 HIGHEST-VALUE INVOICES ==========")
print("Invoice Number | Total Sales (£)")

for invoice, total in top_invoice.items():
    print(f"{invoice} | £{total:,.2f}")

# =======================================
# IVNVESTIGATE HIGHEST -VALUE INVOICES
# =======================================

# Select invoice 581483
invoice_details = explore_data[
    explore_data["InvoiceNo"].astype(str) == "581483"
].copy()

# Display the invoice details
print("================ INVESTIGATING INVOICE 581483 =================")
column_to_show =["InvoiceNo","StockCode","Description","Quantity","UnitPrice","SaleValue","Country"]

display_explore_data = invoice_details[column_to_show]

print(display_explore_data.to_string(index=False))


# Calculate the invoice total
invoice_total = invoice_details["SaleValue"].sum()

print(f"Invoice Total: £{invoice_total:,.2f}")
print("Number of transaction rows:",len(invoice_details))

# ====================================
# VERIFYING INVOICES SALES CALCULATION
# ====================================

invoice = explore_data[
    explore_data["InvoiceNo"].astype(str) == "581483"
]

quantity = invoice["Quantity"].iloc[0]
unit_price = invoice["UnitPrice"].iloc[0]
sales_value = invoice["SaleValue"].iloc[0]

print("======== SALES CALCULATION CHECK =========")
print("Quantity:", quantity)
print(f"Unit Price: £{unit_price:.10f}")
print(f"Recoreded Sales Value: £{sales_value:.2f}")
print(f"Quantity * UnitPrice: £{quantity * unit_price:.2f}")