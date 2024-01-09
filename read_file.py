import pandas as pd

df_data = pd.read_excel('hello.xlsx', index_col=0)
print(df_data.head())

