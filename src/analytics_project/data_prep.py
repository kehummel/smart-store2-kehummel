"""Module 2: Initial Script to Verify Project Setup.

File: src/analytics_project/data_prep.py.
"""

# Imports after the opening docstring

import pathlib

import pandas as pd

# Import local modules (e.g. utils/logger.py)
from analytics_project.utils_logger import logger

# Optional: Use a data_scrubber module for common data cleaning tasks
from analytics_project.utils_scrubber import DataScrubber

# Constants
SCRIPTS_DATA_PREP_DIR: pathlib.Path = (
    pathlib.Path(__file__).resolve().parent
)  # Directory of the current script
SCRIPTS_DIR: pathlib.Path = SCRIPTS_DATA_PREP_DIR.parent  # analytics_project folder
PROJECT_ROOT: pathlib.Path = SCRIPTS_DIR.parent  # src folder
DATA_DIR: pathlib.Path = PROJECT_ROOT / "data"
RAW_DATA_DIR: pathlib.Path = DATA_DIR / "raw"
PREPARED_DATA_DIR: pathlib.Path = DATA_DIR / "prep"


# Define a reusable function that accepts a full path.
def read_and_log(path: pathlib.Path) -> pd.DataFrame:
    """Read a CSV at the given path into a DataFrame, with friendly logging.

    We know reading a csv file can fail
    (the file might not exist, it could be corrupted),
    so we put the statement in a try block.
    It could fail due to a FileNotFoundError or other exceptions.
    If it succeeds, we log the shape of the DataFrame.
    If it fails, we log an error and return an empty DataFrame.
    """
    try:
        # Typically, we log the start of a file read operation
        logger.info(f"Reading raw data from {path}.")
        df = pd.read_csv(path)
        # Typically, we log the successful completion of a file read operation
        logger.info(
            f"{path.name}: loaded DataFrame with shape {df.shape[0]} rows x {df.shape[1]} cols"
        )
        return df
    except FileNotFoundError:
        logger.error(f"File not found: {path}")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Error reading {path}: {e}")
        return pd.DataFrame()


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


def clean_sales_data(df: pd.DataFrame):
    logger.info("Cleaning Sales Data")

    initial_shape = df.shape
    logger.info(f"Initial shape: {initial_shape}")


# Define a main function to start our data processing pipeline.


def main() -> None:
    """Process raw data."""
    logger.info("Starting data preparation...")

    # Build explicit paths for each file under data/raw
    customer_path = RAW_DATA_DIR.joinpath("customers_data.csv")
    product_path = RAW_DATA_DIR.joinpath("products_data.csv")
    sales_path = RAW_DATA_DIR.joinpath("sales_data.csv")

    # Call the function once per file
    read_and_log(customer_path)
    read_and_log(product_path)
    read_and_log(sales_path)

    logger.info("Data preparation complete.")


# Standard Python idiom to run this module as a script when executed directly.

if __name__ == "__main__":
    # Initialize logger
    init_logger()

    # Call the main function by adding () after the function name
    main()
