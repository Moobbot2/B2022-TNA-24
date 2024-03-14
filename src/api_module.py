import program_database
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from pyvi import ViUtils
from ultis import get_tc, get_last_modified_model
from config import FEATURES, SAVE_MODEL_PATH, TABLE_NAME
app = Flask(__name__)
CORS(app)
print(SAVE_MODEL_PATH)
latest_model_path = get_last_modified_model(SAVE_MODEL_PATH)
print(latest_model_path)

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
    trieu_chung = process_symptoms(features)
    print(trieu_chung)
    predictions = loaded_model.predict([trieu_chung])
    print(f'predictions: {predictions}')
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
            print(predict)
            predictions_list = predictions.tolist()
            text_return = "Không bị ung thư"
            if 1 in predictions_list:
                text_return = "Có khả năng bị ung thư"

            return jsonify({'predictions': text_return})
        else:
            return jsonify({'error': 'Invalid JSON format'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def save_symptoms_to_database(symptoms, table_name):
    mydb = program_database.connect_to_database()
    if mydb:
        program_database.insert_data_into_table(mydb, table_name, symptoms)
        return True
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

            save_symptoms_to_database(symptoms, TABLE_NAME)

            return jsonify({'predictions': 'hello'})
        else:
            return jsonify({'error': 'Invalid JSON format'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)
