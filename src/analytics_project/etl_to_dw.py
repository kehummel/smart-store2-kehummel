# Imports at the top

import pathlib
import sqlite3
import sys

import pandas as pd

# Ensure project root is in sys.path for local imports
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))

# Import local modules (e.g. utils/logger.py)
from analytics_project.utils_logger import logger

# Global constants for paths and key directories

THIS_DIR: pathlib.Path = pathlib.Path(__file__).resolve().parent
PACKAGE_DIR: pathlib.Path = THIS_DIR  # src/analytics_project/
SRC_DIR: pathlib.Path = PACKAGE_DIR.parent  # src/
PROJECT_ROOT_DIR: pathlib.Path = SRC_DIR.parent  # smart-store2-kehummel/

# Data directories - now pointing to analytics_project/data
DATA_DIR: pathlib.Path = SRC_DIR / "data"
RAW_DATA_DIR: pathlib.Path = DATA_DIR / "raw"
CLEAN_DATA_DIR: pathlib.Path = DATA_DIR / "prepared"
WAREHOUSE_DIR: pathlib.Path = DATA_DIR / "warehouse"

# Warehouse database location (SQLite)
DB_PATH: pathlib.Path = WAREHOUSE_DIR / "smart_sales.db"

# Recommended - log paths and key directories for debugging

logger.info(f"THIS_DIR:            {THIS_DIR}")
logger.info(f"PACKAGE_DIR:         {PACKAGE_DIR}")
logger.info(f"SRC_DIR:             {SRC_DIR}")
logger.info(f"PROJECT_ROOT_DIR:    {PROJECT_ROOT_DIR}")

logger.info(f"DATA_DIR:            {DATA_DIR}")
logger.info(f"RAW_DATA_DIR:        {RAW_DATA_DIR}")
logger.info(f"CLEAN_DATA_DIR:      {CLEAN_DATA_DIR}")
logger.info(f"WAREHOUSE_DIR:       {WAREHOUSE_DIR}")
logger.info(f"DB_PATH:             {DB_PATH}")


def create_schema(cursor: sqlite3.Cursor) -> None:
    """Create tables in the data warehouse if they don't exist."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer (
            customer_id INTEGER PRIMARY KEY,
            name TEXT,
            region TEXT,
            join_date TEXT,
            number_of_purchases INTEGER,
            contact_preferences TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT,
            category TEXT,
            unit_price REAL,
            stock_quantity INTEGER,
            purchase_type TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sale (
            sales_id INTEGER PRIMARY KEY,
            sale_date TEXT,
            customer_id INTEGER,
            product_id INTEGER,
            store_id INTEGER,
            campaign_id INTEGER,
            sales_amount REAL,
            number_of_items INTEGER,
            city TEXT,
            FOREIGN KEY (customer_id) REFERENCES customer (customer_id),
            FOREIGN KEY (product_id) REFERENCES product (product_id)
        )
   """)


def insert_customers(customers_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Insert customer data into the customer table."""

    # Check what's already in the database
    cursor.execute("SELECT COUNT(*) FROM customer")
    existing_count = cursor.fetchone()[0]
    logger.info(f"Existing rows in customer table: {existing_count}")

    logger.info(f"Attempting to insert {len(customers_df)} customer rows.")

    # Check for duplicates in the dataframe
    duplicates = customers_df[customers_df.duplicated(subset=['customer_id'], keep=False)]
    logger.info(f"Duplicates in DataFrame: {len(duplicates)}")

    if len(duplicates) > 0:
        logger.warning(f"Duplicate customer_ids found: {duplicates['customer_id'].tolist()}")
        logger.warning(f"Full duplicate rows:\n{duplicates}")
        # Remove duplicates
        customers_df = customers_df.drop_duplicates(subset=['customer_id'], keep='first')
        logger.info(f"After removing duplicates: {len(customers_df)} rows remaining")

    customers_df.to_sql("customer", cursor.connection, if_exists="append", index=False)


def insert_products(products_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Insert product data into the product table."""
    logger.info(f"Inserting {len(products_df)} product rows.")
    products_df.to_sql("product", cursor.connection, if_exists="append", index=False)


def insert_sales(sales_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Insert sales data into the sales table."""
    logger.info(f"Inserting {len(sales_df)} sale rows.")

    # Check for duplicates
    duplicates = sales_df[sales_df.duplicated(subset=['sales_id'], keep=False)]
    logger.info(f"Duplicates in DataFrame: {len(duplicates)}")

    if len(duplicates) > 0:
        logger.warning(f"Duplicate sales_ids found: {duplicates['sales_id'].unique().tolist()}")
        # Remove duplicates
        sales_df = sales_df.drop_duplicates(subset=['sales_id'], keep='first')
        logger.info(f"After removing duplicates: {len(sales_df)} rows remaining")

    sales_df.to_sql("sale", cursor.connection, if_exists="append", index=False)


def load_data_to_db() -> None:
    """Load clean data into the data warehouse."""
    logger.info("Starting ETL: loading clean data into the warehouse.")

    # Make sure the warehouse directory exists
    WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)

    # If an old database exists, remove and recreate with the latest table definitions.
    if DB_PATH.exists():
        logger.info(f"Removing existing warehouse database at: {DB_PATH}")
        DB_PATH.unlink()

    # Initialize a connection variable
    # before the try block so we can close it in finally
    conn: sqlite3.Connection | None = None

    try:
        # Connect to SQLite. Create the file if it doesn't exist
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create schema and clear existing records
        create_schema(cursor)

        # Load prepared data using pandas
        customers_df = pd.read_csv(CLEAN_DATA_DIR.joinpath("customers_prepared.csv"))
        products_df = pd.read_csv(CLEAN_DATA_DIR.joinpath("products_prepared.csv"))
        sales_df = pd.read_csv(CLEAN_DATA_DIR.joinpath("sales_prepared.csv"))

        # Insert data into the database for all tables

        insert_customers(customers_df, cursor)

        insert_products(products_df, cursor)

        insert_sales(sales_df, cursor)

        conn.commit()
        logger.info("ETL finished successfully. Data loaded into the warehouse.")
    finally:
        # Regardless of success or failure, close the DB connection if it exists
        if conn is not None:
            logger.info("Closing database connection.")
            conn.close()


if __name__ == "__main__":
    load_data_to_db()
