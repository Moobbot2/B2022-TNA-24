import cv2
import numpy as np
from PIL import Image, ImageEnhance


def preprocess(img, factor: int):
    """Preprocess the image to enhance contrast and sharpness"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = Image.fromarray(img)
    enhancer = ImageEnhance.Sharpness(img).enhance(factor)
    if gray.std() < 30:
        enhancer = ImageEnhance.Contrast(enhancer).enhance(factor)
    return np.array(enhancer)


def binarize_image(img):
    """Convert the image to binary"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh, img_bin = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    img_bin = 255 - img_bin
    return img_bin


def detect_horizontal_lines(img_bin, kernel_len):
    """Detect horizontal lines in the table"""
    hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))
    image_horizontal = cv2.erode(img_bin, hor_kernel, iterations=3)
    horizontal_lines = cv2.dilate(image_horizontal, hor_kernel, iterations=3)
    return horizontal_lines


def group_horizontal_lines(h_lines, thin_thresh):
    """Group closely located horizontal lines"""
    new_h_lines = []
    while len(h_lines) > 0:
        thresh = sorted(h_lines, key=lambda x: x[0][1])[0][0]
        lines = [
            line
            for line in h_lines
            if thresh[1] - thin_thresh <= line[0][1] <= thresh[1] + thin_thresh
        ]
        h_lines = [
            line
            for line in h_lines
            if thresh[1] - thin_thresh > line[0][1]
            or line[0][1] > thresh[1] + thin_thresh
        ]
        x = []
        for line in lines:
            x.append(line[0][0])
            x.append(line[0][2])
        x_min, x_max = min(x) - int(5 * thin_thresh), max(x) + int(5 * thin_thresh)
        new_h_lines.append([x_min, thresh[1], x_max, thresh[1]])
    return new_h_lines


def detect_vertical_lines(img_bin, kernel_len):
    """Detect vertical lines in the table"""
    ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))
    image_vertical = cv2.erode(img_bin, ver_kernel, iterations=3)
    vertical_lines = cv2.dilate(image_vertical, ver_kernel, iterations=3)
    return vertical_lines


def group_vertical_lines(v_lines, thin_thresh):
    """Group closely located vertical lines"""
    new_v_lines = []
    while len(v_lines) > 0:
        thresh = sorted(v_lines, key=lambda x: x[0][0])[0][0]
        lines = [
            line
            for line in v_lines
            if thresh[0] - thin_thresh <= line[0][0] <= thresh[0] + thin_thresh
        ]
        v_lines = [
            line
            for line in v_lines
            if thresh[0] - thin_thresh > line[0][0]
            or line[0][0] > thresh[0] + thin_thresh
        ]
        y = []
        for line in lines:
            y.append(line[0][1])
            y.append(line[0][3])
        y_min, y_max = min(y) - int(4 * thin_thresh), max(y) + int(4 * thin_thresh)
        new_v_lines.append([thresh[0], y_min, thresh[0], y_max])
    return new_v_lines


def seg_intersect(line1: list, line2: list):
    """Calculate intersection points of lines"""
    a1, a2 = line1
    b1, b2 = line2
    da = a2 - a1
    db = b2 - b1
    dp = a1 - b1

    def perp(a):
        b = np.empty_like(a)
        b[0] = -a[1]
        b[1] = a[0]
        return b

    dap = perp(da)
    denom = np.dot(dap, db)
    num = np.dot(dap, dp)
    return (num / denom.astype(float)) * db + b1


def get_bottom_right(right_points, bottom_points, points):
    """Get bottom right corner points of cells"""
    for right in right_points:
        for bottom in bottom_points:
            if [right[0], bottom[1]] in points:
                return right[0], bottom[1]
    return None, None
