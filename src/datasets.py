import pandas as pd
from config import FEATURES, KQ, OUTPUT_LINK
from connect_sql_database import mydb

df = pd.read_excel(OUTPUT_LINK)

X = df[FEATURES]
Y = df[KQ]
