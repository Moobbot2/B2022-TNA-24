# pip install mysql-connector-python
from traceback import print_tb
import mysql.connector
import sys

sys.path.insert(0, "./src")
from config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME


def connect_to_database(
    db_username=DB_USERNAME, db_password=DB_PASSWORD, db_host=DB_HOST, db_name=DB_NAME
):
    try:
        # Creating connection object
        mydb = mysql.connector.connect(
            host=db_host, user=db_username, password=db_password, database=db_name
        )
        return mydb
    except mysql.connector.Error as error:
        print("Error while connecting to MySQL", error)
        return None


def fetch_data_from_table(mydb, table_name):
    try:
        # Creating a cursor
        mycursor = mydb.cursor()

        # Query to fetch data from the table
        query = f"SELECT * FROM {table_name}"

        # Executing the query
        mycursor.execute(query)

        # Fetching all rows from the result
        result = mycursor.fetchall()

        # Closing the cursor
        mycursor.close()

        return result

    except mysql.connector.Error as error:
        print("Error while fetching data from MySQL", error)


def insert_data_into_table(mydb, table_name, data):
    print("----- insert_data_into_table -----")
    try:
        # If data is not already a list of lists, convert it to one
        if not isinstance(data[0], list):
            data = [data]
        # Creating a cursor
        mycursor = mydb.cursor()

        # Query to insert data into the table
        query = f"INSERT INTO {table_name} VALUES ({','.join(['%s'] * len(data[0]))})"

        # Executing the query
        mycursor.executemany(query, data)

        # Commit the transaction
        mydb.commit()

        # Closing the cursor
        mycursor.close()

        print("Data inserted successfully.")

    except mysql.connector.Error as error:
        print("Error while inserting data into MySQL", error)


def main():
    # Example usage:
    table_name = "trieu_chung_va_chuan_doan"
    # data_to_insert = [
    #     (value1, value2, ...),  # Each tuple represents a row of data
    #     (value1, value2, ...),
    #     # Add more rows as needed
    # ]

    mydb = connect_to_database()
    if mydb:
        # insert_data_into_table(mydb, table_name, data_to_insert)
        fetched_data = fetch_data_from_table(mydb, table_name)
        mydb.close()
    else:
        print("Failed to connect to the database.")

    # Printing the fetched data
    for row in fetched_data:
        print(row)


if __name__ == "__main__":
    main()
