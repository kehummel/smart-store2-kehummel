#####################################  # noqa: D100
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


# Constants
SCRIPTS_DATA_PREP_DIR: pathlib.Path = (
    pathlib.Path(__file__).resolve().parent
)  # Directory of the current script
SCRIPTS_DIR: pathlib.Path = SCRIPTS_DATA_PREP_DIR.parent
PROJECT_ROOT: pathlib.Path = SCRIPTS_DIR.parent
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

# Read the csv file


def read_raw_data(file_name: str) -> pd.DataFrame:
    logger.info(f"FUNCTION START: read_raw_data with file_name={file_name}")
    file_path = RAW_DATA_DIR.joinpath(file_name)
    logger.info(f"Reading data from {file_path}")
    df = pd.read_csv(file_path)
    logger.info(f"Loaded dataframe with {len(df)} rows and {len(df.columns)} columns")

    # Add data profiling here to understand the dataset
    # Log the datatypes of each column and the number of unique values

    logger.info(f"Column datatypes: \n{df.dtypes}")
    logger.info(f"Number of unique values: \n{df.nunique()}")

    return df


#####################################
# Define Main Function - The main entry point of the script
#####################################


# Remove duplicates


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"FUNCTION START: remove_duplicates with dataframe shape={df.shape}")
    initial_count = len(df)

    # Drop duplicates
    df = df.drop_duplicates(subset=["TransactionID"])

    removed_count = initial_count - len(df)
    logger.info(f"Removed {removed_count} duplicate rows")
    logger.info(f"{len(df)} records remaining after removing duplicates.")

    return df

    # Handle missing values


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"FUNCTION START: handle_missing_values with dataframe shape={df.shape}")

    # Log missing values by column before handling
    # NA means missing or "not a number" - ask your AI for details
    missing_by_col = df.isna().sum()
    logger.info(f"Missing values by column before handling:\n{missing_by_col}")

    # Implement appropriate missing value handling
    df["TransactionID"] = df["TransactionID"].fillna("NA")
    df["SaleDate"] = df["SaleDate"].fillna("0/0/00")
    df["CustomerID"] = df["CustomerID"].fillna("0")
    df["ProductID"] = df["ProductID"].fillna("0")
    df["StoreID"] = df["StoreID"].fillna('0')
    df["CampaignID"] = df["CampaignID"].fillna("unknown")
    df["SaleAmount"] = pd.to_numeric(df["SaleAmount"], errors='coerce')
    df["SaleAmount"] = df["SaleAmount"].fillna(df["SaleAmount"].median())
    df["NumberofItems"] = df["NumberofItems"].fillna("0")
    df["City"] = df["City"].fillna("unknown")
    df = df.dropna(subset=["TransactionID"])  # Remove rows without transaction ID

    # Log missing values by column after handling
    missing_after = df.isna().sum()
    logger.info(f"Missing values by column after handling:\n{missing_after}")
    logger.info(f"{len(df)} records remaining after handling missing values.")

    return df

    # TODO:Remove outliers


def remove_outliers(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"FUNCTION START: remove_outliers with dataframe shape={df.shape}")
    initial_count = len(df)

    for col in [
        'SaleAmount',
        'NumberofItems',
    ]:
        if col in df.columns and df[col].dtype in ['int64', 'float64']:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
            logger.info(f"Applied outlier removal to {col}: bounds [{lower_bound}, {upper_bound}]")

    removed_count = initial_count - len(df)
    logger.info(f"Removed {removed_count} outlier rows")
    logger.info(f"{len(df)} records remaining after removing outliers.")
    return df


def standardize_formats(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"FUNCTION START: standardize_formats with dataframe shape={df.shape}")

    # Implement standardization for product data
    # Standardizing text fields, units, and categorical variables
    df["SaleAmount"] = df["SaleAmount"].round(2)  # Round prices to 2 decimal places
    df["City"] = df["City"].str.title()
    df["SaleDate"] = pd.to_datetime(df["SaleDate"], errors='coerce')
    df["SaleDate"] = df["SaleDate"].dt.strftime('%m/%d/%Y')

    logger.info("Completed standardizing formats")
    return df

    # Save prepared data


def save_prepared_data(df: pd.DataFrame, file_name: str) -> None:
    logger.info(
        f"FUNCTION START: save_prepared_data with file_name={file_name}, dataframe shape={df.shape}"
    )
    file_path = PREPARED_DATA_DIR.joinpath(file_name)
    df.to_csv(file_path, index=False)
    logger.info(f"Data saved to {file_path}")


#####################################
# Conditional Execution Block
# Ensures the script runs only when executed directly
# This is a common Python convention.
#####################################
def main() -> None:
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

    # Record original shape
    original_shape = df.shape

    # Log initial dataframe information
    logger.info(f"Initial dataframe columns: {', '.join(df.columns.tolist())}")
    logger.info(f"Initial dataframe shape: {df.shape}")

    # Clean column names
    original_columns = df.columns.tolist()
    df.columns = df.columns.str.strip()

    # Log if any column names changed
    changed_columns = [
        f"{old} -> {new}" for old, new in zip(original_columns, df.columns) if old != new
    ]
    if changed_columns:
        logger.info(f"Cleaned column names: {', '.join(changed_columns)}")

    # Remove Duplicates
    df = remove_duplicates(df)

    # Handle Missing Values
    df = handle_missing_values(df)

    # Remove Outliers
    df = remove_outliers(df)

    # Standardizing the Format
    df = standardize_formats(df)

    # Save prepared data
    save_prepared_data(df, output_file)

    logger.info("==================================")
    logger.info(f"Original shape: {original_shape}")
    logger.info(f"Cleaned shape:  {df.shape}")
    logger.info("==================================")
    logger.info("FINISHED prepare_sales_data.py")
    logger.info("==================================")


# -------------------
# Conditional Execution Block
# -------------------

if __name__ == "__main__":
    main()
