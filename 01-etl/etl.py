# Imports
import pandas as pd

# Initialize data source 1
file1 = pd.ExcelFile("ETLDataSource1.xlsx")
order_source_1 = file1.parse("orderSource1") # alt: order_source_1 = pd.read_excel('ETLDataSource1.xlsx', sheet_name='orderSource1')
product_source_1 = file1.parse("productSource1")
state_lookup_source_1 = file1.parse("StateLookup", index_col=1)
file1.close()

# Initialize data source 2
file2 = pd.ExcelFile("ETLDataSource2.xlsx")
order_source_2 = file2.parse("orderSource2")
product_source_2 = file2.parse("productSource2")
file2.close()

# Join both data sources
data_source_1 = pd.merge(order_source_1, product_source_1, on="OrderID")
data_source_2 = pd.merge(order_source_2, product_source_2, on="OrderID")

# Replace state abbrevations with full name in data source 1
state_lookup_dict = state_lookup_source_1.to_dict()["State"]
data_source_1["CustomerState"] = data_source_1["CustomerState"].map(state_lookup_dict)

# Split attribute CustomerName to CustomerFirstName and CustomerLastName in data source 1
data_source_1[["CustomerFirstName", "CustomerLastName"]] = data_source_1["CustomerName"].str.split(' ', 1, expand=True)

# Remove CustomerName attribute in data source 1
data_source_1 = data_source_1.drop(columns=["CustomerName"]) # alt: .drop(["CustomerName"], axis=1)

# Reorder attributes in data source 1 (TODO)

# Replace 'A' in OrderID with null in data source 2
data_source_2["OrderID"] = data_source_2["OrderID"].str.replace('A','')

# Parse OrderID data type from string to int in data source 2
data_source_2["OrderID"] = pd.to_numeric(data_source_2["OrderID"])

# Replace CustomerStatus numerical with full name in data source 2
customer_status_dict = {1: "Silver", 2: "Gold", 3: "Platinum"}
data_source_2["CustomerStatus"] = data_source_2["CustomerStatus"].map(customer_status_dict)

# Remove TotalDiscount attribute in data source 2
data_source_2 = data_source_2.drop(columns=["TotalDiscount"])

# Generate TotalDiscount in data source 2 where TotalDiscount = FullPrice * Discount
data_source_2["TotalDiscount"] = data_source_2["FullPrice"] - data_source_2["ExtendedPrice"]

# Reorder attributes in data source 2 (TODO)

# Concat data sources
data_sources = pd.concat([data_source_1, data_source_2])

# Combine CustomerFirstName and CustomerLastName to CustomerName
data_sources["CustomerName"] = data_sources["CustomerFirstName"] + " " + data_sources["CustomerLastName"]

# Remove CustomerFirstName and CustomerLastName attributes
data_sources = data_sources.drop(columns=["CustomerFirstName", "CustomerLastName"])

# Write to Excel
data_sources.to_excel("PythonResult.xlsx")