import numpy as np
import pandas as pd
import io
import easyocr
from pdf2image import convert_from_path
import cv2

# Khởi tạo mô hình EasyOCR
reader = easyocr.Reader(['vi'])

# Đường dẫn đến tài liệu PDF chứa bảng
pdf_path = "./dataset/cham_soc.pdf"

# Sử dụng pdf2image để chuyển các trang PDF thành hình ảnh
pages = convert_from_path(
    pdf_path, poppler_path=r"./poppler-24.02.0/Library/bin")

# Duyệt qua từng trang và trích xuất văn bản từ ảnh sử dụng EasyOCR
for i, page in enumerate(pages):
    # Convert page to numpy array
    page_np = np.array(page)

    # Use EasyOCR to extract text and bounding boxes from the numpy array
    result = reader.readtext(page_np)

    # Draw bounding boxes on the image
    for detection in result:
        # Extract bounding box coordinates
        bbox = detection[0]

        # Convert bounding box coordinates to integers
        bbox = [(int(x), int(y)) for x, y in bbox]

        # Draw bounding box on the image
        cv2.rectangle(page_np, bbox[0], bbox[2], (0, 255, 0), 2)

    # Save the image with bounding boxes
    cv2.imwrite(f"./output/page_{i+1}_with_boxes.jpg", page_np)

# Print message
print("Bounding boxes drawn and saved.")
