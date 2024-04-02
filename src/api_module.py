from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from pyvi import ViUtils
from ultis import get_tc, get_last_modified_model
from config import FEATURES, SAVE_MODEL_PATH, TABLE_NAME, MODEL_USE
import program
from datasets import X, Y, mydb
import sys

sys.path.insert(0, "./src_database")
import program_database

app = Flask(__name__)
CORS(app)

latest_model_path = get_last_modified_model(SAVE_MODEL_PATH, MODEL_USE)
print(f"Load model: {latest_model_path}")

if latest_model_path:
    loaded_model = joblib.load(latest_model_path)
    print("Loaded model from:", latest_model_path)
    loaded_model.feature_names = FEATURES
else:
    print("No model found in the directory.")


def preprocess_feature(feature):
    feature_without_accents_bytes = ViUtils.remove_accents(feature.lower())
    feature_without_accents = feature_without_accents_bytes.decode('utf-8')
    return feature_without_accents


def process_symptoms(features):
    preprocessed_symptoms = [preprocess_feature(
        feature) for feature in features]
    symptoms = get_tc(preprocessed_symptoms)
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


@app.route('/api_predict', methods=['POST'])
def api_predict():
    try:
        if request.is_json:
            data = request.get_json()
            trieu_chung = data.get('features', [])
            print('===========================')
            print('trieu_chung:', trieu_chung)
            print('===========================')
            predictions = predict(trieu_chung)
            text_return = "Không bị ung thư" if predictions[0] == 0 else "Có khả năng bị ung thư"
            return jsonify({'predictions': text_return})
        else:
            return jsonify({'error': 'Invalid JSON format'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def save_symptoms_to_database(symptoms, table_name):
    try:
        mydb = program_database.connect_to_database()
        if mydb:
            program_database.insert_data_into_table(mydb, table_name, symptoms)
            return True
        return False
    except Exception as e:
        print("Error saving symptoms to database:", str(e))
        return False


@app.route('/api_save_data', methods=['POST'])
def api_save_data():
    try:
        if request.is_json:
            data = request.get_json()
            features = data.get('features', [])
            print('===========================')
            print('features:', features)
            print('===========================')
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
                return jsonify({'predictions': 'Đã cập nhật.'}), 200
            else:
                return jsonify({'error': 'Failed to save symptoms to database'}), 500
        else:
            return jsonify({'error': 'Invalid JSON format'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api_update_module', methods=['POST'])
def api_update_module():
    try:
        mydb
        program.train_evaluate_visualize_decision_tree(
            X, Y, classifier_type='DecisionTree')
        return jsonify({'message': 'Cập nhật model thành công!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Nhiều triệu chứng vào => Sinh ra độ đo đánh giá


if __name__ == '__main__':
    app.run(port=5000, debug=True)
