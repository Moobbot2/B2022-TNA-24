import sys
from flask import Flask, request, jsonify
import flask
from flask_cors import CORS
import joblib
import numpy as np
from pdf2image import convert_from_bytes
from tools.utils import get_local_ip
from unidecode import unidecode

from config.config import FEATURES, FEATURES_VN, MODEL_USE, POPPLER_PATH, SAVE_MODEL_PATH, TABLE_NAME
from src.cancer_diagnosis.helpers import get_last_modified_model, get_symptoms
from src.cancer_diagnosis.training import train_evaluate_visualize_decision_tree
from src.connect_database.database_utils import insert_data_into_table
from src.connect_database import load_data
from src.ocr_medical_record.ocr_data import process_page

app = Flask(__name__)
CORS(app)

sys.setrecursionlimit(40000)

latest_model_path = get_last_modified_model(SAVE_MODEL_PATH, MODEL_USE)

if latest_model_path:
    loaded_model = joblib.load(latest_model_path)
    print("Loaded model from:", latest_model_path)
    loaded_model.feature_names = FEATURES
else:
    print("No model found in the directory.")


def preprocess_feature(feature):
    feature_lower = feature.lower()
    feature_unidecode = unidecode(feature_lower)
    return feature_unidecode


def process_symptoms(features):
    preprocessed_symptoms = [preprocess_feature(feature) for feature in features]
    symptoms = get_symptoms(preprocessed_symptoms)
    return symptoms


def map_predictions_to_features(predictions, feature_names):
    result = [[1 if feature in predictions else 0 for feature in feature_names]]
    return result


def predict(features):
    p_s = process_symptoms(features)
    if 1 not in p_s:
        return [0]
    print("process_symptoms:", p_s)
    predictions = loaded_model.predict([p_s])
    print("predictions:", predictions)
    return predictions


@app.route("/api_predict", methods=["POST"])
def api_predict():
    try:
        if request.is_json:
            data = request.get_json()
            trieu_chung = data.get("features", [])
            print("===========================")
            print("trieu_chung:", trieu_chung)
            print("===========================")
            predictions = predict(trieu_chung)

            text_return = (
                "Không bị ung thư" if predictions[0] == 0 else "Có khả năng bị ung thư"
            )
            return jsonify({"predictions": text_return})
        else:
            return jsonify({"error": "Invalid JSON format"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def save_symptoms_to_database(symptoms, table_name):
    try:
        mydb = load_data.mydb
        if mydb:
            insert_data_into_table(mydb, table_name, symptoms)
            return True
        return False
    except Exception as e:
        print("Error saving symptoms to database:", str(e))
        return False


@app.route("/api_save_data", methods=["POST"])
def api_save_data():
    try:
        if request.is_json:
            data = request.get_json()
            features = data.get("features", [])
            print("===========================")
            print("features:", features)
            print("===========================")
            # Extract the last feature as the result
            ket_qua_str = features[-1]

            # Convert the string result to an integer
            ket_qua = int(ket_qua_str)

            # Preprocess the symptoms
            symptoms = process_symptoms(features[:-1])

            # Append the preprocessed result
            symptoms.append(ket_qua)
            print(symptoms)
            # Attempt to save symptoms to the database
            if save_symptoms_to_database(symptoms, TABLE_NAME):
                return jsonify({"predictions": "Đã cập nhật."}), 200
            else:
                return jsonify({"error": "Failed to save symptoms to database"}), 500
        else:
            return jsonify({"error": "Invalid JSON format"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api_update_module", methods=["POST"])
def api_update_module():
    try:
        train_evaluate_visualize_decision_tree(
            load_data.X, load_data.Y, classifier_type="DecisionTree"
        )
        return jsonify({"message": "Cập nhật model thành công!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def ocr_symptoms(pdf_byte, column_to_extract=3):

    pages = convert_from_bytes(pdf_byte, poppler_path=POPPLER_PATH)
    extracted_data = []
    text_status = ""
    # Process each page
    for i, page in enumerate(pages):
        text_extract = process_page(np.array(page), i + 1, column_to_extract)
        extracted_data.append(text_extract)
        text_status += text_extract

    text_status = text_status.lower()
    text_status = unidecode(text_status)
    symptoms = get_symptoms(text_status)
    return symptoms


@app.route("/api_medical_record", methods=["POST"])
def api_medical_record():
    try:
        if flask.request.method == "POST":
            if "file_pdf" not in request.files:
                return jsonify({"error": "No PDF file uploaded"}), 400

            pdf_file = flask.request.files["file_pdf"].read()
            file_name = flask.request.form.get("file_name")

            column_to_extract = 3  # Mặc định là 3 (File chăm sóc)
            if file_name == "cham_soc":
                column_to_extract = 3
            if file_name == "dieu_tri":
                column_to_extract = 2
            symptoms = ocr_symptoms(pdf_file, column_to_extract)
            text_symptoms = []

            for index, symptom_status in enumerate(symptoms):
                if symptom_status == 1:
                    text_symptoms.append(FEATURES_VN[index])
            return jsonify({"symptoms": text_symptoms})
    except Exception as e:
        print("Error in api_medical_record:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    HOST_CONNECT = get_local_ip()
    PORT_CONNECT = 5000
    app.run(host= HOST_CONNECT, port=PORT_CONNECT, debug=True)
