"""
scripts/data_preparation/prepare_sales.py

This script reads data from the data/raw folder, cleans the data,
and writes the cleaned version to the data/prepared folder.

Tasks:
- Remove duplicates
- Handle missing values
- Remove outliers
- Ensure consistent formatting

"""

#####################################
# Import Modules at the Top
#####################################

# Import from Python Standard Library
import pathlib
import sys

# Import from external packages (requires a virtual environment)
import pandas as pd

# Ensure project root is in sys.path for local imports (now 3 parents are needed)
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent.parent))

# Import local modules (e.g. utils/logger.py)
from analytics_project.utils_logger import logger

# Optional: Use a data_scrubber module for common data cleaning tasks
from analytics_project.utils_scrubber import DataScrubber


# Constants
SCRIPTS_DATA_PREP_DIR: pathlib.Path = (
    pathlib.Path(__file__).resolve().parent
)  # Directory of the current script
SCRIPTS_DIR: pathlib.Path = SCRIPTS_DATA_PREP_DIR.parent  # analytics project
PROJECT_ROOT: pathlib.Path = SCRIPTS_DIR.parent  # scr
DATA_DIR: pathlib.Path = PROJECT_ROOT / "data"
RAW_DATA_DIR: pathlib.Path = DATA_DIR / "raw"
PREPARED_DATA_DIR: pathlib.Path = DATA_DIR / "prepared"  # place to store prepared data


# Ensure the directories exist or create them
DATA_DIR.mkdir(exist_ok=True)
RAW_DATA_DIR.mkdir(exist_ok=True)
PREPARED_DATA_DIR.mkdir(exist_ok=True)

#####################################
# Define Functions - Reusable blocks of code / instructions
#####################################


def read_raw_data(file_name: str) -> pd.DataFrame:
    """
    Read raw data from CSV.

    Args:
        file_name (str): Name of the CSV file to read.

    Returns:
        pd.DataFrame: Loaded DataFrame.
    """
    logger.info(f"FUNCTION START: read_raw_data with file_name={file_name}")
    file_path = RAW_DATA_DIR.joinpath(file_name)
    logger.info(f"Reading data from {file_path}")
    df = pd.read_csv(file_path)
    logger.info(f"Loaded dataframe with {len(df)} rows and {len(df.columns)} columns")

    logger.info(f"Column datatypes: \n{df.dtypes}")
    logger.info(f"Number of unique values: \n{df.nunique()}")

    return df


def save_prepared_data(df: pd.DataFrame, file_name: str) -> None:
    """
    Save cleaned data to CSV.

    Args:
        df (pd.DataFrame): Cleaned DataFrame.
        file_name (str): Name of the output file.
    """
    logger.info(
        f"FUNCTION START: save_prepared_data with file_name={file_name}, dataframe shape={df.shape}"
    )
    file_path = PREPARED_DATA_DIR.joinpath(file_name)
    df.to_csv(file_path, index=False)
    logger.info(f"Data saved to {file_path}")


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows from the DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: DataFrame with duplicates removed.
    """
    logger.info(f"FUNCTION START: remove_duplicates with dataframe shape={df.shape}")

    # Let's delegate this to the DataScrubber class
    # First, create an instance of the DataScrubber class
    # by passing in the dataframe as an argument.
    df_scrubber = DataScrubber(df)

    # Now, call the method on our instance to remove duplicates.
    # This method will return a new dataframe with duplicates removed.
    df_deduped = df_scrubber.remove_duplicate_records()

    logger.info(f"Original dataframe shape: {df.shape}")
    logger.info(f"Deduped  dataframe shape: {df_deduped.shape}")
    return df_deduped


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    # Change column names to match the standard formatting

    logger.info("Function Start: rename_columns")

    # Log columns BEFORE renaming
    logger.info(f"Columns BEFORE renaming: {df.columns.tolist()}")

    column_mapping = {
        "TransactionID": "transaction_id",
        "SaleDate": "sale_date",
        "CustomerID": "customer_id",
        "ProductID": "product_id",
        "StoreID": "store_id",
        "CampaignID": "campaign_id",
        "SaleAmount": "sales_amount",
        "NumberofItems": "number_of_items",
        "City": "city",
    }

    df = df.rename(columns=column_mapping)
    # Log columns AFTER renaming
    logger.info(f"Columns AFTER renaming: {df.columns.tolist()}")
    logger.info("Function End: rename_columns")
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values by filling or dropping.
    This logic is specific to the actual data and business rules.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: DataFrame with missing values handled.
    """
    logger.info(f"FUNCTION START: handle_missing_values with dataframe shape={df.shape}")

    # Log missing values by column before handling
    # NA means missing or "not a number" - ask your AI for details
    missing_by_col = df.isna().sum()
    logger.info(f"Missing values by column before handling:\n{missing_by_col}")

    df["sale_date"] = df["sale_date"].fillna("05/04/2025")
    df["customer_id"] = df["customer_id"].fillna(0)
    df["product_id"] = df["product_id"].fillna(0)
    df = df.dropna(subset=["transaction_id"])  # Remove rows without a transaction ID
    df["store_id"] = df["store_id"].fillna(399)
    df["campaign_id"] = df["campaign_id"].fillna(100)
    df["sales_amount"] = df["sales_amount"].fillna(0)
    df["number_of_items"] = df["number_of_items"].fillna(0)
    df["city"] = df["city"].fillna("unknown city")

    # Log missing values by column after handling
    missing_after = df.isna().sum()
    logger.info(f"Missing values by column after handling:\n{missing_after}")
    logger.info(f"{len(df)} records remaining after handling missing values.")
    return df


def standardize_formats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize the formatting of various columns.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: DataFrame with standardized formatting.
    """
    logger.info(f"FUNCTION START: standardize_formats with dataframe shape={df.shape}")

    # DEBUG: Print columns to see what we have
    logger.info(f"Columns in standardize_formats: {df.columns.tolist()}")
    print(f"DEBUG - Columns: {df.columns.tolist()}")  # Also print to console

    # First, convert to datetime using dayfirst=True to handle YYYY-DD-MM format
    df['sale_date'] = pd.to_datetime(
        df['sale_date'], format='mixed', dayfirst=True, errors='coerce'
    )

    # Then convert to your desired string format: MM/DD/YYYY
    df['sale_date'] = df['sale_date'].dt.strftime('%m/%d/%Y')

    df['city'] = df['city'].str.lower()  # Lowercase for categories

    # Convert to numeric before rounding
    df["sales_amount"] = pd.to_numeric(df["sales_amount"], errors='coerce')
    df["sales_amount"] = df["sales_amount"].round(2)  # Round prices to 2 decimal places

    # Convert campaign_id to numeric first, then to int
    df["campaign_id"] = pd.to_numeric(df["campaign_id"], errors='coerce')
    df["campaign_id"] = df["campaign_id"].astype('Int64')  # Use nullable integer

    # Convert number_of_items to numeric first, then to int
    df["number_of_items"] = pd.to_numeric(df["number_of_items"], errors='coerce')
    df["number_of_items"] = df["number_of_items"].astype('Int64')  # Use nullable integer

    logger.info("Completed standardizing formats")
    return df


def remove_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove outliers based on thresholds.
    This logic is very specific to the actual data and business rules.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: DataFrame with outliers removed.
    """
    logger.info(f"FUNCTION START: remove_outliers with dataframe shape={df.shape}")
    initial_count = len(df)

    # Convert to numeric (in case it's stored as strings)
    df["number_of_items"] = pd.to_numeric(df["number_of_items"], errors='coerce')

    # Now filter
    df = df[(df["number_of_items"] < 8)]

    removed_count = initial_count - len(df)
    logger.info(f"Removed {removed_count} outlier rows")
    logger.info(f"{len(df)} records remaining after removing outliers.")
    return df


#####################################
# Define Main Function - The main entry point of the script
#####################################


def main() -> None:
    """
    Main function for processing data.
    """
    logger.info("==================================")
    logger.info("STARTING prepare_sales_data.py")
    logger.info("==================================")

    logger.info(f"Root         : {PROJECT_ROOT}")
    logger.info(f"data/raw     : {RAW_DATA_DIR}")
    logger.info(f"data/prepared: {PREPARED_DATA_DIR}")
    logger.info(f"scripts      : {SCRIPTS_DIR}")

    input_file = "sales_data.csv"
    output_file = "sales_prepared.csv"

    # Read raw data
    df = read_raw_data(input_file)

    # Clean column names (strip whitespace) FIRST
    original_columns = df.columns.tolist()
    df.columns = df.columns.str.strip()  # ← Make sure this runs!

    # Log if any column names changed
    changed_columns = [
        f"{old} -> {new}" for old, new in zip(original_columns, df.columns) if old != new
    ]
    if changed_columns:
        logger.info(f"Cleaned column names: {', '.join(changed_columns)}")

    # Record original shape
    original_shape = df.shape

    # Log initial dataframe information
    logger.info(f"Initial dataframe columns: {', '.join(df.columns.tolist())}")
    logger.info(f"Initial dataframe shape: {df.shape}")

    # Remane columns
    df = rename_columns(df)

    # Remove duplicates
    df = remove_duplicates(df)

    # Standardize Column Data
    df = standardize_formats(df)

    # Handle missing values
    df = handle_missing_values(df)

    # Remove outliers
    df = remove_outliers(df)

    # Save prepared data
    save_prepared_data(df, output_file)

    logger.info("==================================")
    logger.info(f"Original shape: {df.shape}")
    logger.info(f"Cleaned shape:  {original_shape}")
    logger.info("==================================")
    logger.info("FINISHED prepare_sales_data.py")
    logger.info("==================================")


#####################################
# Conditional Execution Block
# Ensures the script runs only when executed directly
# This is a common Python convention.
#####################################

if __name__ == "__main__":
    main()
