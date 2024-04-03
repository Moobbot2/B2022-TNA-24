import joblib
import numpy as np
from pdf2image import convert_from_path
from unidecode import unidecode

from helpers import add_path_init  # Helper function to add custom module paths

# Adding custom module paths to sys.path
add_path_init()
from cancer_diagnosis.helpers import get_last_modified_model, get_symptoms
from config import FEATURES, SAVE_MODEL_PATH, MODEL_USE, POPPLER_PATH
from ocr_medical_record.ocr_data import process_page

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
    pages = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)

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
    TMP = get_symptoms(text_status)
    print(TMP)
    predictions = loaded_model.predict([TMP])
    print(predictions)


if __name__ == "__main__":
    main()
