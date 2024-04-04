from config.config import (
    DB_HOST,
    DB_NAME,
    DB_PASSWORD,
    DB_USERNAME,
    FEATURES,
    KQ,
    TABLE_NAME,
)
from src.connect_database import database_utils
from tools.utils import create_dataframe_from_table_data

try:
    mydb = database_utils.connect_to_database(
        db_host=DB_HOST,
        db_name=DB_NAME,
        db_username=DB_USERNAME,
        db_password=DB_PASSWORD,
    )
    column_names = FEATURES + [KQ]
    data_table = database_utils.fetch_data_from_table(mydb, TABLE_NAME)
    df = create_dataframe_from_table_data(data_table, column_names)
    X = df[FEATURES]
    Y = df[KQ]
except:
    X = FEATURES
    Y = [KQ]
