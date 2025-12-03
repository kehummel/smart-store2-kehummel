"""
scripts/project_7/scrub_customers.py

This script reads customer data from the data/prepared folder and writes the cleaned version to the data_p7 folder.

It originally came from Denise Case's smart-sales-raw-data file: https://github.com/denisecase/smart-sales-raw-data/blob/main/data/raw/customers_data.csv

Tasks:
- Remove duplicates
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
SMARTSTORE2_FOLDER: pathlib.Path = PROJECT_7_FOLDER.parent  # smartstore2 folder
SRC_FOLDER: pathlib.Path = SMARTSTORE2_FOLDER / "src"  # src folder
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
    """Read raw data from CSV."""
    file_path: pathlib.Path = RAW_DATA_DIR.joinpath(file_name)
    try:
        logger.info(f"READING: {file_path}.")
        return pd.read_csv(file_path)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return pd.DataFrame()  # Return an empty DataFrame if the file is not found
    except Exception as e:
        logger.error(f"Error reading {file_path}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame if any other error occurs


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


def column_data_type(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Function Start: Changing Data Type")

    scrubber = DataScrubber(df)

    df = scrubber.convert_column_to_new_data_type('customer_id', int)
    logger.info(f"Converted column 'customer_id' to dtype: {df['customer_id'].dtype}")

    df = scrubber.convert_column_to_new_data_type("number_of_purchases", int)
    logger.info(f"Converted column 'customer_id' to dtype: {df["number_of_purchases"].dtype}")

    df['join_date'] = pd.to_datetime(df['join_date'], errors='coerce')
    logger.info(f"Converted column 'join_date' to dtype: {df['join_date'].dtype}")
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows from the DataFrame.
    How do you decide if a row is duplicated?
    Which do you keep? Which do you delete?

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
    df_deduped = df_scrubber.remove_duplicate_records(subset=["customer_id"], keep="first")

    logger.info(f"Original dataframe shape: {df.shape}")
    logger.info(f"Deduped  dataframe shape: {df_deduped.shape}")
    return df_deduped


#####################################
# Define Main Function - The main entry point of the script
#####################################


def main() -> None:
    """
    Main function for processing customer data.
    """
    logger.info("==================================")
    logger.info("STARTING prepare_customers_data.py")
    logger.info("==================================")

    input_file = "customers_prepared.csv"
    output_file = "customer_cube_prep.csv"

    # Read raw data
    df = read_raw_data(input_file)

    # Record original shape
    original_shape = df.shape

    # Log initial dataframe information
    logger.info(f"Initial dataframe columns: {', '.join(df.columns.tolist())}")
    logger.info(f"Initial dataframe shape: {df.shape}")

    # Remove duplicates
    df = remove_duplicates(df)

    # Data Typees
    df = column_data_type(df)

    # Save prepared data
    save_prepared_data(df, output_file)

    logger.info("==================================")
    logger.info(f"Original shape: {df.shape}")
    logger.info(f"Cleaned shape:  {original_shape}")
    logger.info("==================================")
    logger.info("FINISHED prepare_customers_data.py")
    logger.info("==================================")


#####################################
# Conditional Execution Block
# Ensures the script runs only when executed directly
# This is a common Python convention.
#####################################

if __name__ == "__main__":
    main()
