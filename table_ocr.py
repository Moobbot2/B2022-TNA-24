import joblib
import numpy as np
import cv2
import os
from pdf2image import convert_from_path
from unidecode import unidecode
from tools.program import (
    preprocess,
    binarize_image,
    detect_horizontal_lines,
    group_horizontal_lines,
    detect_vertical_lines,
    group_vertical_lines,
    seg_intersect,
    get_bottom_right,
)
import easyocr
import logging
from src.ultis import get_last_modified_model, get_tc
from src.config import FEATURES, SAVE_MODEL_PATH, MODEL_USE

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize EasyOCR reader
reader = easyocr.Reader(["vi"])

# Define constants
KERNEL_DIVISOR = 120
MAX_LINE_GAP = 250
OUTPUT_FOLDER = "./output/table_ocr"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Create output/cell subfolder if it doesn't exist
CELL_OUTPUT_FOLDER = os.path.join(OUTPUT_FOLDER, "cell")
os.makedirs(CELL_OUTPUT_FOLDER, exist_ok=True)


# Function to process a single page
def process_page(page, page_number, column_to_extract=3):
    logger.info(f"Processing page {page_number}")
    # Preprocess page
    enhanced_page = preprocess(page, factor=5)
    img_bin = binarize_image(enhanced_page)

    # Detect horizontal and vertical lines
    kernel_len = img_bin.shape[1] // KERNEL_DIVISOR
    horizontal_lines = detect_horizontal_lines(img_bin, kernel_len)
    vertical_lines = detect_vertical_lines(img_bin, kernel_len)

    # Group lines
    h_lines = cv2.HoughLinesP(
        horizontal_lines, 1, np.pi / 180, 30, maxLineGap=MAX_LINE_GAP
    )
    v_lines = cv2.HoughLinesP(
        vertical_lines, 1, np.pi / 180, 30, maxLineGap=MAX_LINE_GAP
    )
    new_horizontal_lines = group_horizontal_lines(h_lines, kernel_len)
    new_vertical_lines = group_vertical_lines(v_lines, kernel_len)

    # Find intersection points and draw rectangles around cells
    print("Find intersection points")
    points = []
    for hline in new_horizontal_lines:
        x1A, y1A, x2A, y2A = hline
        for vline in new_vertical_lines:
            x1B, y1B, x2B, y2B = vline

            line1 = [np.array([x1A, y1A]), np.array([x2A, y2A])]
            line2 = [np.array([x1B, y1B]), np.array([x2B, y2B])]

            x, y = seg_intersect(line1, line2)
            if x1A <= x <= x2A and y1B <= y <= y2B:
                points.append([int(x), int(y)])

    print("Draw rectangles around cells")

    # Draw rectangles around cells
    cells = []
    for point in points:
        left, top = point
        right_points = sorted(
            [p for p in points if p[0] > left and p[1] == top], key=lambda x: x[0]
        )
        bottom_points = sorted(
            [p for p in points if p[1] > top and p[0] == left], key=lambda x: x[1]
        )

        right, bottom = get_bottom_right(right_points, bottom_points, points)
        if right and bottom:
            cv2.rectangle(enhanced_page, (left, top), (right, bottom), (0, 0, 255), 2)
            cells.append([left, top, right, bottom])

    print("Crop cells and save")
    # Crop cells and save
    prev_left = cells[0][0]
    row_counter = 1
    col_counter = 0
    cells_data = []
    for i, cell in enumerate(cells):
        left, top, right, bottom = cell
        if int(left) == int(prev_left) and i != 0:
            row_counter += 1
            col_counter = 1
        else:
            col_counter += 1
        if col_counter == column_to_extract and row_counter > 1:
            cell_image = page[top:bottom, left:right]
            cell_filename = f"page_{page_number}_cell_{row_counter}_{col_counter}.jpg"
            cell_filepath = os.path.join(CELL_OUTPUT_FOLDER, cell_filename)
            cv2.imwrite(cell_filepath, cell_image)
            cells_data.append(cell)
    # out_img_link = os.path.join(OUTPUT_FOLDER, f"page_{page_number}.jpg")
    # cv2.imwrite(out_img_link, enhanced_page)

    print("Start ocr text")
    # Perform OCR on extracted cells
    extracted_text = ""
    for cell in cells_data:
        cell_x_min, cell_y_min, cell_x_max, cell_y_max = cell
        cell_image = page[cell_y_min:cell_y_max, cell_x_min:cell_x_max]
        cell_image_rgb = cv2.cvtColor(cell_image, cv2.COLOR_BGR2RGB)
        # Read text from cell using EasyOCR
        horizontal_list = reader.readtext(cell_image_rgb, detail=0)
        text_cell = " ".join(horizontal_list)
        corrected_text = text_cell.replace("không", ", không")
        corrected_text = corrected_text.replace(",,", ",")
        corrected_text = corrected_text.replace(";", ",")
        extracted_text = " ".join([extracted_text, corrected_text])
        logger.info(f"Extracted text from cell: {extracted_text}")
    return extracted_text


latest_model_path = get_last_modified_model(SAVE_MODEL_PATH, MODEL_USE)
print(f"Load model: {latest_model_path}")

if latest_model_path:
    loaded_model = joblib.load(latest_model_path)
    print("Loaded model from:", latest_model_path)
    loaded_model.feature_names = FEATURES
else:
    print("No model found in the directory.")




def main():
    # Đường dẫn đến tài liệu PDF chứa bảng
    pdf_path = "./dataset/cham_soc.pdf"

    # Sử dụng pdf2image để chuyển các trang PDF thành hình ảnh
    pages = convert_from_path(pdf_path, poppler_path=r"./poppler-24.02.0/Library/bin")

    # Chăm sóc lấy cột 3, điều trị lấy cột 2
    column_to_extract = 3

    extracted_data = []
    text_status = ""
    # Process each page
    for i, page in enumerate(pages):
        text_extract = process_page(np.array(page), i + 1, column_to_extract)
        extracted_data.append(text_extract)
        text_status += text_extract

    text_status = text_status.lower()
    text_status = unidecode(text_status)
    TMP = get_tc(text_status)
    print(TMP)
    predictions = loaded_model.predict([TMP])
    print(predictions)


if __name__ == "__main__":
    main()
