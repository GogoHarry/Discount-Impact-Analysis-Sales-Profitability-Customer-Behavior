# Import required libraries
import pandas as pd  # Pandas for data manipulation and handling CSV files
import logging  # Logging module to capture errors
from sqlalchemy import create_engine  # SQLAlchemy for database connection and execution

# Configure logging to capture errors in 'error.log' file
logging.basicConfig(filename='error.log', level=logging.ERROR, format="%(asctime)s = %(message)s")

# Database credentials and connection parameters
db_user = 'root'  # MySQL username
db_password = 'Password'  # MySQL password
db_host = 'localhost'  # Database server host (localhost for local machine)
db_name = 'e-commerce'  # Database name

# Creating MySQL connection using SQLAlchemy
engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}')

# Define file paths for the CSV datasets
csv_files = {
    'customer': 'cleaned_customer.csv',  # Path to cleaned customer data
    'product': 'cleaned_product.csv',  # Path to cleaned product data
    'transaction': 'cleaned_transaction.csv'  # Path to cleaned transaction data
}

# Define primary keys for each dataset to check for duplicate records
primary_keys = {
    'customer': 'CustomerID',  # Primary key for customer data
    'product': 'ProductID',  # Primary key for product data
    'transaction': 'TransactionID'  # Primary key for transaction data
}

# Function to load CSV data into MySQL and avoid inserting duplicates
def csv_to_sql(table_name, file_path, primary_key):
    """
    Reads a CSV file, compares it with existing data in the database, 
    and appends only new records based on the primary key.

    Parameters:
    table_name (str): The name of the table in the database.
    file_path (str): Path to the CSV file.
    primary_key (str): Column name that serves as the primary key for duplicate checking.
    """
    try:
        # Read data from CSV file
        df = pd.read_csv(file_path)

        # Fetch existing records from the database
        existing_df = pd.read_sql(f'SELECT * FROM {table_name}', con=engine)

        # Identify new records by checking if primary key values exist in the database
        new_data = df[~df[primary_key].isin(existing_df[primary_key])]

        # If new data exists, append it to the database
        if not new_data.empty:
            new_data.to_sql(table_name, con=engine, if_exists='append', index=False)
            print(f'{len(new_data)} new records added to the {table_name} table.')
        else:
            print(f'No new records found for {table_name}.')

    except Exception as e:
        # Log and print any errors encountered during execution
        logging.error(f'Error syncing {table_name}: {str(e)}')
        print(f'Error syncing {table_name}')

# Main function to iterate through the CSV files and load them into the database
def main():
    """
    Iterates through the list of CSV files and syncs each with the corresponding MySQL table.
    """
    for table, file in csv_files.items():
        csv_to_sql(table, file, primary_keys[table])

    print('All CSV files synced successfully.')

# Entry point of the script
if __name__ == '__main__':
    main()
