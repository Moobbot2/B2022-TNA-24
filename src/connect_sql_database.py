# Importing module
import mysql.connector
from config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME
# Creating connection object
mydb = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USERNAME,
    password=DB_PASSWORD,
    database=DB_NAME
)

# Printing the connection object
print(mydb)
