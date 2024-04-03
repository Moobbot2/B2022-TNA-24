# Importing necessary functions and modules
from helpers import add_path_init  # Helper function to add custom module paths

add_path_init()  # Adding custom module paths to sys.path

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

print("Check connect db")
mydb = program_database.connect_to_database(
    db_host=DB_HOST,
    db_name=DB_NAME,
    db_username=DB_USERNAME,
    db_password=DB_PASSWORD,
)
print(mydb)

data_table = program_database.fetch_data_from_table(mydb, TABLE_NAME)

column_names = FEATURES + [KQ]
df = create_dataframe_from_table_data(data_table, column_names)
print(df)

program_database.write_dataframe_to_database(
    df,
    db_host=DB_HOST,
    db_name=DB_NAME,
    db_username=DB_USERNAME,
    db_password=DB_PASSWORD,
    table_name=TABLE_NAME,
)
data = [[1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0]]
program_database.insert_data_into_table(mydb, TABLE_NAME, data)
