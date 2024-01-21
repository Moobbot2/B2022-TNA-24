from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS extension
import joblib
import numpy as np
from pyvi import ViUtils
from ultis import get_tc
from config import FEATURES, KQ, OUTPUT_LINK

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

global feature_names

# Load the decision tree model
loaded_model = joblib.load('model/cart_tree_model.joblib')
loaded_model.feature_names = FEATURES


def preprocess_feature(feature):
    # Use ViUtils.remove_accents to remove accents from Vietnamese characters
    feature_without_accents_bytes = ViUtils.remove_accents(feature.lower())
    feature_without_accents = feature_without_accents_bytes.decode('utf-8')

    return feature_without_accents


def map_predictions_to_features(predictions, feature_names):
    # Create a list of values (1 if feature is in predictions, 0 otherwise)
    result = [[1 if feature in predictions else 0 for feature in feature_names]]
    return result


def predict(tc):
    tc_preprocess = [preprocess_feature(
        feature) for feature in tc]
    trieu_chung = get_tc(tc_preprocess)
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

            # Convert NumPy array to list
            predictions_list = predictions.tolist()
            text_return = "Không bị ung thư"
            if 1 in predictions_list:
                text_return = "Có khả năng bị ung thư"

            return jsonify({'predictions': text_return})
        else:
            return jsonify({'error': 'Invalid JSON format'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)
