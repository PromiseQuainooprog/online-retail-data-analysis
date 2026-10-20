# ==========================================
# ANALYSLAB AFRICA INTERSIP PROJECT
# WEEK 1-2: DATA CLEANING
#  Dataset: Online Retail Dataset
# ==========================================

# Import the required libraries
import pandas as pd
import os 

# ---------------------------------
# 1. Load the original Dataset
# ---------------------------------

raw_data = pd.read_csv("../raw/OnlineRetail.csv",encoding="ISO-8859-1")

print("Raw data shape:", raw_data.shape)

# Preserve the original dataset in memory
raw_rows = len(raw_data)

# ==============================
# 2. DATA CLEANING AND PROCESSING
# ===============================

# --------------------------------------------------
# 1. Create a separate copy of the original dataset
# ----------------------------------------------------

clean_data = raw_data.copy()

# ---------------------------------------------
# 2. Check missing values before cleaning
# ------------------------------------------

print("Missing values before cleaning:",clean_data.isnull().sum())

# ----------------------------
# 3. Standardize column names
# -----------------------------
clean_data.columns = (clean_data.columns
              .str.strip()
              .str.replace(" ","", regex=False))

print("Standardized column names:",clean_data.columns.tolist())

# -------------------------------------
# 4. Standardize Text Fields
# -----------------------------------

for column in ["Description", "Country"]:
    if column in clean_data.columns:
        clean_data[column] = clean_data[column].apply(
            lambda value: ( value.strip() 
                           if isinstance(value, str) 
                           else value)
        )

# ---------------------------------
# 5. Convert InvoiceDate to DateTime
# -----------------------------------

clean_data["InvoiceDate"] = pd.to_datetime(
    clean_data["InvoiceDate"], errors="coerce")

clean_data["Quantity"] = pd.to_numeric(clean_data["Quantity"], errors="coerce")

clean_data["UnitPrice"] = pd.to_numeric(clean_data["UnitPrice"], errors="coerce")

# -------------------------------
# 6. Identity Duplicate Records
# ----------------------------------

print("Duplicate Rows:", clean_data.duplicated().sum())

# Remove exact duplicate rows 
clean_data = clean_data.drop_duplicates().copy()
print("Shape after duplicate removed:", clean_data.shape)
print("Row after duplicate removed:", len(clean_data))

# -----------------------------------------
# 7. Validate Quantities and Prices
# ----------------------------------------

# Checking unsual quantites
print("Negative quantities:", (clean_data["Quantity"]<0).sum())
print("Zero quantities:", (clean_data["Quantity"]==0).sum())

# Checking unsual prices
print("Negative prices:", (clean_data["UnitPrice"]<0).sum())
print("Zero prices:", (clean_data["UnitPrice"]==0).sum())

# Remove records with missing or inalid numerical transaction values
clean_data = clean_data.dropna(
    subset=["Quantity","UnitPrice"]).copy()

clean_data = clean_data[
    (clean_data["Quantity"] !=0) &
    (clean_data["UnitPrice"] >=0)
 ].copy()

# Negative quantities are retained because they may represent cancellation or product returns.

# ------------------------------------
# 8. Inestigate Inalid Dates
# ----------------------------------
invalid_dates = clean_data["InvoiceDate"].isna().sum()

print("Missing or invalid invoice dates:", invalid_dates)

# Exclude records that cannot support time-based
# or reliable transaction analysis.
clean_data = clean_data.dropna(subset=["InvoiceDate"]).copy()

# ------------------------------------
# 9. Create a Transaction Value Coulmn
# --------------------------------------

clean_data["SaleValue"] = clean_data["Quantity"] * clean_data["UnitPrice"]

# This is a sihned line value, not necessarily recognized revenue. Negative quantities can represent return or cancellation.

# -------------------------------------
# 10. Report Final Cleaning Results
# -----------------------------------
print("Final dataset shape:", clean_data.shape)

print("Remaining missing values:", clean_data.isnull().sum())

print("Rows in original dataset:", raw_rows)

print("Rows in cleaned dataset:", len(clean_data))

print("Total rows removed:", raw_rows - len(clean_data))

# --------------------------------------
# 11. Save a Cleaning CheckPoint
# ----------------------------------

# Create the folder pathif it does not exist
os.makedirs("data/processed", exist_ok=True)

# --------------------------------------
# 12. Save tye cleaned dataset separately
# -----------------------------------------

clean_data.to_csv(
    "data/processed/OnlineRetail.csv",
    index=False)
print("Cleaned dataset saved successfully!")
