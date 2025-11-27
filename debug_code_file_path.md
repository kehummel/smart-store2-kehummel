## Code to run to see if you are going down the correct path to retreive your data, and output it in the correct spot. 

def main():
    """Execute OLAP cubing process."""
    logger.info("Starting OLAP Cubing process...")

    # DEBUG: Detailed path checking
    logger.info(f"Database file exists: {DB_PATH.exists()}")
    logger.info(f"Database is a file: {DB_PATH.is_file()}")
    logger.info(f"Parent directory exists: {DB_PATH.parent.exists()}")

    # Check if we can read the file
    import os
    try:
        logger.info(f"Can read database: {os.access(DB_PATH, os.R_OK)}")
        logger.info(f"Can write to database: {os.access(DB_PATH, os.W_OK)}")
        logger.info(f"File size: {DB_PATH.stat().st_size} bytes")
    except Exception as e:
        logger.error(f"Error checking file access: {e}")
