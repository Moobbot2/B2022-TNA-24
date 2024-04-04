# pip install mysql-connector-python
import mysql.connector
from sqlalchemy import create_engine


def connect_to_database(db_host, db_name, db_username, db_password):
    print("connect_to_database")
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


def write_dataframe_to_database(
    df, db_host, db_name, db_username, db_password, table_name
):
    engine = create_engine(
        f"mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_name}"
    )
    try:
        df.to_sql(table_name, con=engine, if_exists="append", index=False)
        print("Data written to the database successfully.")
    except Exception as e:
        print("Error occurred while writing data to the database:", e)
