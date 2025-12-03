"""Project 7: Cubing Script.

DIMENSION TABLES

Sales Table
    product ID - Primary Key
    customer ID
    Sales ID
    sales amount
    city name

Products Table
    Category
    Product ID

Customer Table
    Customer ID
    Join Date

OUTPUT TABLE
    Category
    City
    Year
    Sales Amount
    Sales Amount Sum
    Sales Amount Mean
    Sales Amount Count
    Days Since Joined
    Time Since Joined
"""

import pandas as pd
import pathlib

from analytics_project.utils_logger import logger

# Constants
PROJECT_7_FOLDER = pathlib.Path(__file__).resolve().parent  # project_7 folder
SMARTSTORE2_FOLDER = PROJECT_7_FOLDER.parent  # smartstore2 folder
DATA_FOLDER = PROJECT_7_FOLDER / "data_p7"  # folder containing csvs

# Output directories
DATA_DIR = PROJECT_7_FOLDER / "data_p7"
PREPARED_DATA_DIR = DATA_DIR  # OUTPUT directly to data_p7

# Ensure the directories exist or create them
DATA_DIR.mkdir(exist_ok=True)

# Read your CSVs
sales = pd.read_csv(
    DATA_FOLDER / 'sales_cube_prep.csv',
    usecols=["product_id", "customer_id", "sales_id", "sales_amount", "city"],
)
customers = pd.read_csv(
    DATA_FOLDER / 'customer_cube_prep.csv', usecols=["customer_id", "join_date"]
)
products = pd.read_csv(DATA_FOLDER / 'products_cube_prep.csv', usecols=["category", "product_id"])
logger.info("csvs Read")

# Merge them together
cube_df = sales.merge(customers, on='customer_id').merge(products, on='product_id')
logger.info("Cube Created")

# Convert join_date to datetime (do this once, before all date operations)
cube_df['join_date'] = pd.to_datetime(cube_df['join_date'])

# Calculate time since join date
today = pd.Timestamp.now()
cube_df['days_since_join'] = (today - cube_df['join_date']).dt.days


# Calculate years and months since join
def calculate_time_elapsed(join_date):
    delta = today - join_date
    years = delta.days // 365
    remaining_days = delta.days % 365
    months = remaining_days // 30
    return f"{years} year(s) and {months} month(s)"


cube_df['time_since_join'] = cube_df['join_date'].apply(calculate_time_elapsed)

# Add year column
cube_df["year"] = cube_df["join_date"].dt.year
logger.info("Created time_since_join and year columns")

# Create aggregated cube
# Include the new columns in your aggregation
cube = (
    cube_df.groupby(['category', 'city', 'year', "sales_amount"])
    .agg(
        {
            'sales_amount': ['sum', 'mean', 'count'],
            'days_since_join': 'first',  # Take first value since it's same per customer
            'time_since_join': 'first',  # Take first value since it's same per customer
        }
    )
    .reset_index()
)
logger.info("Cube Aggregated")

# Flatten column names after aggregation
cube.columns = ['_'.join(col).strip('_') if col[1] else col[0] for col in cube.columns.values]

# Save the cube to the data directory
output_path = DATA_DIR / 'p7_cube.csv'
cube.to_csv(output_path, index=False)
logger.info(f"Cube saved to: {output_path}")
