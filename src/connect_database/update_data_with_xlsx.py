import pandas as pd
from sqlalchemy import create_engine
from unidecode import unidecode
try:
    from config.config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME
except:
    from config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME

# Đường dẫn tới tệp Excel
excel_file = 'dataset/output.xlsx'

# Đọc dữ liệu từ tệp Excel
df = pd.read_excel(excel_file)

for col in df.columns:
    new_col = unidecode(col).replace(' ', '_')
    df.rename(columns={col: new_col}, inplace=True)
print(df)

# Tạo đối tượng kết nối đến cơ sở dữ liệu
engine = create_engine(
    f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')

# Tên bảng cơ sở dữ liệu
table_name = 'trieu_chung_va_chuan_doan'

# Ghi dữ liệu vào cơ sở dữ liệu
df.to_sql(table_name, con=engine, if_exists='append', index=False)
