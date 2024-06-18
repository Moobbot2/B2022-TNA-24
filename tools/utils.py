import pandas as pd
import socket


def get_local_ip():
    """Get the local IP address of the machine."""
    try:
        # Connect to an external host to get the local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        s.connect(("8.8.8.8", 1))  # Example using Google DNS
        IP_CONNECT = s.getsockname()[0]
        s.close()
    except Exception:
        IP_CONNECT = "127.0.0.1"
    return IP_CONNECT


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
