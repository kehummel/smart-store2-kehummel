"""
scripts/project_7/scrub_sales.py

This script reads data from the data/raw folder, cleans the data, and writes the cleaned version to the data_p7 folder.

It originally came from Denise Case's smart-sales-raw-data file: https://github.com/denisecase/smart-sales-raw-data/blob/main/data/raw/sales_data.csv

Tasks:
- Remove duplicates
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
PROJECT_7_FOLDER: pathlib.Path = pathlib.Path(__file__).resolve().parent  # project_7 folder
REPO_ROOT: pathlib.Path = PROJECT_7_FOLDER.parent  # smart-store2-kehummel folder
SRC_FOLDER: pathlib.Path = REPO_ROOT / "src"  # src folder
RAW_DATA_DIR: pathlib.Path = SRC_FOLDER / "data" / "prepared"  # INPUT location

# Output directories
DATA_DIR: pathlib.Path = PROJECT_7_FOLDER / "data_p7"
PREPARED_DATA_DIR: pathlib.Path = DATA_DIR  # OUTPUT directly to data_p7

# Ensure the directories exist or create them
DATA_DIR.mkdir(exist_ok=True)

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
    df_deduped = df_scrubber.remove_duplicate_records(subset=["sales_id"], keep="first")

    logger.info(f"Original dataframe shape: {df.shape}")
    logger.info(f"Deduped  dataframe shape: {df_deduped.shape}")
    return df_deduped


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

    # Convert to numeric before rounding
    df["sales_amount"] = pd.to_numeric(df["sales_amount"], errors='coerce')
    df["sales_amount"] = df["sales_amount"].round(2)  # Round prices to 2 decimal places

    # Convert product ID to an int
    df["product_id"] = df["product_id"].astype('Int64')

    # Convert Sales ID to an int
    df["sales_id"] = df["sales_id"].astype('Int64')

    # Convert customer ID to int
    df["customer_id"] = df["customer_id"].astype('Int64')

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
    df["sales_amount"] = pd.to_numeric(df["sales_amount"], errors='coerce')

    # Now filter
    df = df[(df["sales_amount"] > 1)]

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

    input_file = "sales_prepared.csv"
    output_file = "sales_cube_prep.csv"

    # Read raw data
    df = read_raw_data(input_file)

    # Clean column names (strip whitespace) FIRST
    df.columns = df.columns.str.strip()  # ← Make sure this runs!

    # Record original shape
    original_shape = df.shape

    # Log initial dataframe information
    logger.info(f"Initial dataframe columns: {', '.join(df.columns.tolist())}")
    logger.info(f"Initial dataframe shape: {df.shape}")

    # Standardize formats of columns
    df = standardize_formats(df)

    # Remove duplicates
    df = remove_duplicates(df)

    # Remove outliers
    df = remove_outliers(df)

    # Save prepared data
    save_prepared_data(df, output_file)

    logger.info("==================================")
    logger.info(f"Original shape: {original_shape}")
    logger.info(f"Cleaned shape:  {df.shape}")
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
