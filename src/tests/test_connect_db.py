# Importing necessary functions and modules
from helpers import add_path_init  # Helper function to add custom module paths

# Adding custom module paths to sys.path
add_path_init()

from config import (
    FEATURES,
    KQ,
    DB_HOST,
    DB_NAME,
    DB_PASSWORD,
    DB_USERNAME,
    TABLE_NAME,
)
from utils import create_dataframe_from_table_data

from connect_database import program_database


# Function to test database connection
def test_database_connection():
    print("Check connect db")
    mydb = program_database.connect_to_database(
        db_host=DB_HOST,
        db_name=DB_NAME,
        db_username=DB_USERNAME,
        db_password=DB_PASSWORD,
    )
    if mydb:
        print("Database connection successful.")
        return mydb
    else:
        print("Failed to connect to the database.")


# Function to fetch data from the database
def test_fetch_data():
    mydb = test_database_connection()
    data_table = program_database.fetch_data_from_table(mydb, TABLE_NAME)
    if data_table:
        print("Data fetched successfully.")
        return data_table
    else:
        print("Failed to fetch data from the database.")


# Function to create DataFrame from fetched data
def test_create_dataframe():
    column_names = FEATURES + [KQ]
    data_table = test_fetch_data()
    df = create_dataframe_from_table_data(data_table, column_names)
    if df is not None:
        print("DataFrame created successfully.")
        print(df.head())  # Print the first few rows of the DataFrame
        return df
    else:
        print("Failed to create DataFrame.")


# Function to write DataFrame back to the database
def test_write_to_database():
    df = test_create_dataframe()
    program_database.write_dataframe_to_database(
        df,
        db_host=DB_HOST,
        db_name=DB_NAME,
        db_username=DB_USERNAME,
        db_password=DB_PASSWORD,
        table_name=TABLE_NAME,
    )


# Function to insert data into the database
def test_insert_data():
    mydb = test_database_connection()
    data = [[1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0]]
    program_database.insert_data_into_table(mydb, TABLE_NAME, data)
    print("Data inserted into the database.")


# Main function to run tests based on user input
def main():
    while True:
        print("===== $$$ =====")
        print("\nChoose an option:")
        print("1. Test database connection")
        print("2. Test create DataFrame")
        print("3. Test write to database")
        print("4. Test insert data")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            test_database_connection()
        elif choice == "2":
            test_create_dataframe()
        elif choice == "3":
            test_write_to_database()
        elif choice == "4":
            test_insert_data()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
    main()
