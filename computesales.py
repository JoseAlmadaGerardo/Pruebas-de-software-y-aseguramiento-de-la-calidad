"""
Computes sales data from JSON files and saves results.
"""

import json
import time
import pandas as pd

start_time = time.time()

# Load ProductList JSON
try:
    with open("TC1.ProductList.json", "r", encoding="utf-8") as f:
        product_list_data = json.load(f)
except FileNotFoundError:
    print("Error: TC1.ProductList.json not found.")
    product_list_data = []

# Load TC1 Sales JSON
try:
    with open("TC1.Sales.json", "r", encoding="utf-8") as f:
        TC1_sales_data = json.load(f)
except FileNotFoundError:
    print("Error: TC1.Sales.json not found.")
    TC1_sales_data = []

# Load TC2 Sales JSON
try:
    with open("TC2.Sales.json", "r", encoding="utf-8") as f:
        TC2_sales_data = json.load(f)
except FileNotFoundError:
    print("Error: TC2.Sales.json not found.")
    TC2_sales_data = []

# Load TC3 Sales JSON
try:
    with open("TC3.Sales.json", "r", encoding="utf-8") as f:
        TC3_sales_data = json.load(f)
except FileNotFoundError:
    print("Error: TC3.Sales.json not found.")
    TC3_sales_data = []

# Create dataframe for ProductList
product_list_df = pd.DataFrame(product_list_data)
product_list_df = product_list_df[[
    'title', 'type', 'description', 'filename',
    'height', 'width', 'price', 'rating']]
product_list_df.columns = [
    'Title', 'Type', 'Description', 'Filename',
    'Height', 'Width', 'Price', 'Rating']

# Save TC1 product list dataframe to priceCatalogue.json
product_list_df.to_json("PriceCatalogue.json", orient="records", indent=2)

# Create dataframe for TC1 Sales
TC1_sales_df = pd.DataFrame(TC1_sales_data)
TC1_sales_df.columns = ['SALE_ID', 'SALE_Date', 'Product', 'Quantity']
TC1_sales_with_price_df = pd.merge(TC1_sales_df, product_list_df[[
    'Title', 'Price']], left_on='Product', right_on='Title', how='left')
TC1_sales_with_price_df.drop(columns=['Title'], inplace=True)

# Create dataframe for TC2 Sales
TC2_sales_df = pd.DataFrame(TC2_sales_data)
TC2_sales_df.columns = ['SALE_ID', 'SALE_Date', 'Product', 'Quantity']
TC2_sales_with_price_df = pd.merge(TC2_sales_df, product_list_df[[
    'Title', 'Price']], left_on='Product', right_on='Title', how='left')
TC2_sales_with_price_df.drop(columns=['Title'], inplace=True)

# Create dataframe for TC3 Sales
TC3_sales_df = pd.DataFrame(TC3_sales_data)
TC3_sales_df.columns = ['SALE_ID', 'SALE_Date', 'Product', 'Quantity']
TC3_sales_with_price_df = pd.merge(TC3_sales_df, product_list_df[[
    'Title', 'Price']], left_on='Product', right_on='Title', how='left')
TC3_sales_with_price_df.drop(columns=['Title'], inplace=True)

# Calculate the TC1 total cost for sales
TC1_sales_with_price_df['Total Cost'] = TC1_sales_with_price_df[
    'Quantity'] * TC1_sales_with_price_df['Price']
TC1_total_cost = TC1_sales_with_price_df['Total Cost'].sum()

# Calculate the TC2 total cost for each sale
TC2_sales_with_price_df['Total Cost'] = TC2_sales_with_price_df[
    'Quantity'] * TC2_sales_with_price_df['Price']
TC2_total_cost = TC2_sales_with_price_df['Total Cost'].sum()

# Calculate the total cost for each sale
TC3_sales_with_price_df['Total Cost'] = TC3_sales_with_price_df[
    'Quantity'] * TC3_sales_with_price_df['Price']
TC3_total_cost = TC3_sales_with_price_df['Total Cost'].sum()

# Save merged dataframe to salesRecord.json
all_sales_df = pd.concat([
    TC1_sales_with_price_df,
    TC2_sales_with_price_df,
    TC3_sales_with_price_df])
all_sales_df.to_json("SalesRecord.json", orient="records", indent=2)

# Save total costs to SalesResults.txt
with open("SalesResults.txt", "w", encoding="utf-8") as f:
    f.write(f"TC1 Total Cost of all sales: {TC1_total_cost}\n")
    f.write(f"TC2 Total Cost of all sales: {TC2_total_cost}\n")
    f.write(f"TC3 Total Cost of all sales: {TC3_total_cost}\n")

# Print TC1 total cost for sales
print("\nTotal Cost of all sales for TC1:", TC1_total_cost)
print()
print("TC1_Sales top DataFrame with Total Cost:")
print(TC1_sales_with_price_df.head())
print("TC1 Sales botom DataFrame Total Cost:")
print(TC1_sales_with_price_df.tail())
print('----------------------------------------------------------------------')
print()

# Print TC2 total cost for sales
print("\n  TC2_Total Cost of all sales:", TC2_total_cost)
print()
print(" TC2 Sales top DataFrame with Total Cost:")
print(TC2_sales_with_price_df.head())
print(" TC2 Sales botom DataFrame with Total Cost:")
print(TC2_sales_with_price_df.tail())
print('----------------------------------------------------------------------')
print()

# Calculate and print the total cost
print("\n TC3_Total Cost of all sales:", TC3_total_cost)
print()
print("TC3 Sales top of DataFrame with Total Cost:")
print(TC3_sales_with_price_df.head())
print("TC3 Sales botom DataFrame with Total Cost:")
print(TC3_sales_with_price_df.tail())
print('----------------------------------------------------------------------')
print()

elapsed_time = time.time() - start_time

# Append elapsed time to SalesResults.txt
with open("SalesResults.txt", "a", encoding="utf-8") as f:
    f.write(f"Time elapsed: {elapsed_time} seconds")
print("Results saved SalesRecord.json, PriceCatalogue.json, SalesResults.txt")
print(f"Time elapsed: {elapsed_time} seconds")
