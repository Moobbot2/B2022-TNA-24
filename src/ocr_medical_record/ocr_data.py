import os
import sys

__dir__ = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(__dir__, "../../"))
sys.path.append(project_root)

import numpy as np
import cv2
import os
import easyocr
import logging
from src.ocr_medical_record.helpers import (
    preprocess,
    binarize_image,
    detect_horizontal_lines,
    group_horizontal_lines,
    detect_vertical_lines,
    group_vertical_lines,
    seg_intersect,
    get_bottom_right,
)

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


def save_output_image(enhanced_page, page_number):
    out_img_link = os.path.join(OUTPUT_FOLDER, f"page_{page_number}.jpg")
    cv2.imwrite(out_img_link, enhanced_page)


def group_lines(lines):
    grouped_lines = cv2.HoughLinesP(lines, 1, np.pi / 180, 30, maxLineGap=MAX_LINE_GAP)
    return grouped_lines


def detect_lines(img_bin):
    kernel_len = img_bin.shape[1] // KERNEL_DIVISOR
    horizontal_lines = detect_horizontal_lines(img_bin, kernel_len)
    vertical_lines = detect_vertical_lines(img_bin, kernel_len)
    # Group lines
    h_lines = group_lines(horizontal_lines)
    v_lines = group_lines(vertical_lines)
    new_horizontal_lines = group_horizontal_lines(h_lines, kernel_len)
    new_vertical_lines = group_vertical_lines(v_lines, kernel_len)
    return new_horizontal_lines, new_vertical_lines


def find_intersection_points(horizontal_lines, vertical_lines):
    point_data = []
    for hline in horizontal_lines:
        x1A, y1A, x2A, y2A = hline
        for vline in vertical_lines:
            x1B, y1B, x2B, y2B = vline

            line1 = [np.array([x1A, y1A]), np.array([x2A, y2A])]
            line2 = [np.array([x1B, y1B]), np.array([x2B, y2B])]

            x, y = seg_intersect(line1, line2)
            if x1A <= x <= x2A and y1B <= y <= y2B:
                point_data.append([int(x), int(y)])
    return point_data


def draw_rectangle_and_extract_cell(
    points, enhanced_page, page, page_number, column_to_extract, save_cell=False
):
    cell_draw = []
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
            cell_draw.append([left, top, right, bottom])

    prev_left = cell_draw[0][0]
    row_counter = 1
    col_counter = 0
    cells_data = []
    for i, cell in enumerate(cell_draw):
        left, top, right, bottom = cell
        if int(left) == int(prev_left) and i != 0:
            row_counter += 1
            col_counter = 1
        else:
            col_counter += 1
        if col_counter == column_to_extract and row_counter > 1:
            cell_image = page[top:bottom, left:right]
            cell_filename = f"page_{page_number}_cell_{row_counter}_{col_counter}.jpg"
            cells_data.append(cell)
            if save_cell == True:
                cell_filepath = os.path.join(CELL_OUTPUT_FOLDER, cell_filename)
                cv2.imwrite(cell_filepath, cell_image)
    return cells_data


def cell_crop_data(cells, column_to_extract, page, page_number, save_cell=False):
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
            cells_data.append(cell)
            if save_cell == True:
                cell_filepath = os.path.join(CELL_OUTPUT_FOLDER, cell_filename)
                cv2.imwrite(cell_filepath, cell_image)
    return cells_data


def hotfix_ocr(text_ocr):
    corrected_text = text_ocr.replace("không", ", không")
    corrected_text = corrected_text.replace(",,", ",")
    corrected_text = corrected_text.replace(";", ",")
    return corrected_text


def ocr_text(cells_data, page):
    extracted_text = ""
    for cell in cells_data:
        cell_x_min, cell_y_min, cell_x_max, cell_y_max = cell
        cell_image = page[cell_y_min:cell_y_max, cell_x_min:cell_x_max]
        cell_image_rgb = cv2.cvtColor(cell_image, cv2.COLOR_BGR2RGB)
        # Read text from cell using EasyOCR
        horizontal_list = reader.readtext(cell_image_rgb, detail=0)
        text_cell = " ".join(horizontal_list)
        extracted_text = " ".join([extracted_text, text_cell])
    corrected_text = hotfix_ocr(extracted_text)
    # logger.info(f"Extracted text from cell: {corrected_text}")
    return corrected_text


# Function to process a single page
def process_page(page, page_number, column_to_extract=3):
    logger.info(f"Processing page {page_number}")
    # Preprocess page
    enhanced_page = preprocess(page, factor=5)
    img_bin = binarize_image(enhanced_page)

    # Detect horizontal and vertical lines
    new_horizontal_lines, new_vertical_lines = detect_lines(img_bin)

    # Find intersection points and draw rectangles around cells
    points = find_intersection_points(new_horizontal_lines, new_vertical_lines)

    # Draw rectangles around cells
    cells_data = draw_rectangle_and_extract_cell(
        points, enhanced_page, page, page_number, column_to_extract
    )
    save_output_image(enhanced_page, page_number)

    # Perform OCR on extracted cells
    extracted_text = ocr_text(cells_data, page)

    return extracted_text
