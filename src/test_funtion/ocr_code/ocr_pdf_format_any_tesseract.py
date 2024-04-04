# pip install pytesseract Pillow
# pip install pdf2image
# dowlaod tesseract https://github.com/UB-Mannheim/tesseract/wiki
import pytesseract
from pdf2image import convert_from_path
import pandas as pd
import io

# Đường dẫn đến chương trình tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Đường dẫn đến tài liệu PDF chứa bảng
pdf_path = "./dataset/test.pdf"

# Sử dụng pdf2image để chuyển các trang PDF thành hình ảnh
pages = convert_from_path(
    pdf_path, poppler_path=r"../poppler-24.02.0/Library/bin")

# Duyệt qua từng trang và trích xuất văn bản từ ảnh
extracted_text = []
for page in pages:
    text = pytesseract.image_to_string(page)
    extracted_text.append(text)

# Xử lý và biến đổi dữ liệu văn bản thành dạng bảng
# (Có thể cần xử lý thêm tùy thuộc vào định dạng của bảng và độ chính xác của OCR)
tables = [pd.read_csv(io.StringIO(text), delimiter='\t')
          for text in extracted_text if text.strip()]

# Lưu bảng vào tệp Excel hoặc CSV
for i, table in enumerate(tables):
    # Lưu dưới dạng tệp Excel
    excel_filename = f"./output/table_{i+1}.xlsx"
    table.to_excel(excel_filename, index=False)
    print(f"Table {i+1} saved as {excel_filename}")
