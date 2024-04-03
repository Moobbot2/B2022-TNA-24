import os
import sys
import pandas as pd


def add_path_init():
    print("Add src to path.")
    current_directory = os.getcwd()
    directories = ["dataset", "config", "tools", "src"]
    for directory in directories:
        sys.path.insert(0, os.path.join(current_directory, directory))
    print(sys.path)


def create_dataframe_from_table_data(data_table, column_names):
    """
    Create a DataFrame from data fetched from a table.

    Parameters:
        data_table (list of tuples): Data fetched from the table.
        column_names (list of str): Column names for the DataFrame.

    Returns:
        pandas.DataFrame: DataFrame constructed from the fetched data.
    """
    # Check if data fetching was successful and lengths match
    if data_table and len(data_table[0]) == len(column_names):
        df = pd.DataFrame(data_table, columns=column_names)
        return df
    else:
        print("Error: Data table and column names do not match in length.")
        return None
