# import numpy as np
# import cv2
# from matplotlib import pyplot as plt
# import easyocr

# from pdf2image import convert_from_path
# pdf_save_path =
# pages = convert_from_path(
#                 pdf_path=pdf_save_path, poppler_path=POPPLER_PATH)

# -------------------------------------------------
# pip install tabula-py pandas
# pip install JPype1
# pip install openpyxl

import tabula
import pandas as pd

# Đường dẫn đến tài liệu PDF chứa bảng
pdf_path = "./dataset/test.pdf"

# Trích xuất bảng từ tài liệu PDF
tables = tabula.read_pdf(pdf_path, pages='all')

# Lưu bảng vào tệp Excel hoặc CSV
for i, table in enumerate(tables):
    # Lưu dưới dạng tệp Excel
    excel_filename = f"./output/table_{i+1}.xlsx"
    table.to_excel(excel_filename, index=False)
    print(f"Table {i+1} saved as {excel_filename}")

    # Lưu dưới dạng tệp CSV
    csv_filename = f"./output/table_{i+1}.csv"
    table.to_csv(csv_filename, index=False)
    print(f"Table {i+1} saved as {csv_filename}")
