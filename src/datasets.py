import pandas as pd
import program_database
from config import FEATURES, KQ, TABLE_NAME

# Connect to the database
mydb = program_database.connect_to_database()

# Check if connection was successful
if mydb:
    # Fetch data from the table
    data_ungthu = program_database.fetch_data_from_table(mydb, TABLE_NAME)

    # Check if data fetching was successful
    if data_ungthu:
        # Create DataFrame
        column_names = FEATURES + [KQ]  # Replace with actual column names
        df = pd.DataFrame(data_ungthu, columns=column_names)

        # Access features and target variable
        X = df[FEATURES]
        Y = df[KQ]

        # Close database connection
        mydb.close()
    else:
        print("Failed to fetch data from the database.")
else:
    print("Failed to connect to the database.")
