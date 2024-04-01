import numpy as np
import cv2
import os
from pdf2image import convert_from_path
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

reader = easyocr.Reader(["vi"])
# Define constants
KERNEL_DIVISOR = 120
MAX_LINE_GAP = 250

output_folder = "./output/table_ocr"
os.makedirs(output_folder, exist_ok=True)

# Create output/cell subfolder if it doesn't exist
cell_output_folder = os.path.join(output_folder, "cell")
os.makedirs(cell_output_folder, exist_ok=True)
    
# Function to process a single page
def process_page(page, output_folder, page_number):
    # Preprocess page
    enhanced_page = preprocess(page, factor=3)
    img_bin = binarize_image(enhanced_page)

    # Detect horizontal lines
    kernel_len = img_bin.shape[1] // KERNEL_DIVISOR
    horizontal_lines = detect_horizontal_lines(img_bin, kernel_len)
    h_lines = cv2.HoughLinesP(
        horizontal_lines, 1, np.pi / 180, 30, maxLineGap=MAX_LINE_GAP
    )
    new_horizontal_lines = group_horizontal_lines(h_lines, kernel_len)

    # Detect vertical lines
    vertical_lines = detect_vertical_lines(img_bin, kernel_len)
    v_lines = cv2.HoughLinesP(
        vertical_lines, 1, np.pi / 180, 30, maxLineGap=MAX_LINE_GAP
    )
    new_vertical_lines = group_vertical_lines(v_lines, kernel_len)

    print("Find intersection points")
    # Find intersection points
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
    prev_left = cells[0][0]
    print(f"prev_left = {prev_left}")
    row_counter = 1
    col_counter = 0
    table_cc = []
    for i, cell in enumerate(cells):
        left, top, right, bottom = cell
        if int(left) == int(prev_left) and i != 0:
            row_counter += 1
            col_counter = 1
        else:
            col_counter += 1
        if col_counter == 3:
            cell_image = page[top:bottom, left:right]
            cell_filename = f"page_{page_number}_cell_{row_counter}_{col_counter}.jpg"
            cell_filepath = os.path.join(cell_output_folder, cell_filename)
            cv2.imwrite(cell_filepath, cell_image)

    out_img_link = os.path.join(output_folder, f"page_{page_number}.jpg")
    print(f"Save the processed page {out_img_link}")
    # Save the processed page
    cv2.imwrite(out_img_link, enhanced_page)
    
    # print("Start ocr text")
    # final_horizontal_list = []
    # for cell in cells:
    #     cell_x_min, cell_y_min, cell_x_max, cell_y_max = cell
    #     cell_image = page[
    #         cell_y_min:cell_y_max, cell_x_min:cell_x_max
    #     ]  # Use 'page' instead of 'table_image'

    #     # Convert cell image to RGB format
    #     cell_image_rgb = cv2.cvtColor(cell_image, cv2.COLOR_BGR2RGB)

    #     # Read text from cell using EasyOCR
    #     horizontal_list = reader.readtext(cell_image_rgb, detail=0)
    #     print(horizontal_list)
    #     print("--------------")

def main():
    # Đường dẫn đến tài liệu PDF chứa bảng
    pdf_path = "./dataset/cham_soc.pdf"

    # Sử dụng pdf2image để chuyển các trang PDF thành hình ảnh
    pages = convert_from_path(pdf_path, poppler_path=r"./poppler-24.02.0/Library/bin")
    
    # Process each page
    # for i, page in enumerate(pages):
    #     process_page(np.array(page), output_folder, i + 1)
    process_page(np.array(pages[0]), output_folder, 0 + 1)
    


if __name__ == "__main__":
    main()
