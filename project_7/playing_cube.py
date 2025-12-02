import pandas as pd

# Read your CSVs
sales = pd.read_csv('sales.csv')
customers = pd.read_csv('customers.csv')
products = pd.read_csv('products.csv')

# Merge them together
cube_df = sales.merge(customers, on='customer_id').merge(products, on='product_id')

# Create aggregated cube (e.g., sales by product, customer, and date)
cube = (
    cube_df.groupby(['product_id', 'customer_id', 'city'])
    .agg({'sales_amount': ['sum', 'mean', 'count'], 'number_of_items': 'sum'})
    .reset_index()
)

# Save the cube
cube.to_csv('sales_cube.csv', index=False)


## and then for just the specfic columns

# Only read specific columns from each CSV
sales = pd.read_csv(
    'sales.csv',
    usecols=['sales_id', 'customer_id', 'product_id', 'sales_amount', 'number_of_items'],
)

customers = pd.read_csv('customers.csv', usecols=['customer_id', 'city', 'join_date'])

products = pd.read_csv('products.csv', usecols=['product_id', 'product_name', 'category'])
