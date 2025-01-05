import os
import sys

__dir__ = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(__dir__, "../../"))
sys.path.append(project_root)

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import datetime

from sklearn.tree import DecisionTreeClassifier
import xgboost as xgb

from src.cancer_diagnosis.helpers import (
    save_model_with_timestamp,
    save_tree_with_timestamp,
    visualize_tree,
)
from src.cancer_diagnosis.metrics import evaluate_performance
from config.config import (
    FEATURES,
    N_ESTIMATORS,
    RAMDOM_STATE,
    SAVE_LOG_PATH,
    SAVE_MODEL_PATH,
    SAVE_TREE_PATH,
    TEST_SIZE,
)
from tools.logging import save_log_model


def train_evaluate_visualize_decision_tree(
    X,
    Y,
    classifier_type,
    save_model_path=SAVE_MODEL_PATH,
    save_tree_path=SAVE_TREE_PATH,
):
    if classifier_type == "DecisionTree":
        classifier = DecisionTreeClassifier()
    elif classifier_type == "RandomForest":
        classifier = RandomForestClassifier(
            n_estimators=N_ESTIMATORS, random_state=RAMDOM_STATE
        )
    elif classifier_type == "XGBoost":
        classifier = xgb.XGBClassifier(
            objective="binary:logistic", random_state=RAMDOM_STATE
        )

    # Chia dữ liệu thành tập huấn luyện và tập kiểm thử
    if len(X) > 1:
        X_train, X_test, y_train, y_test = train_test_split(
        X, Y, test_size=TEST_SIZE, random_state=RAMDOM_STATE
        )
    else:
        print("Not enough data for splitting.")
        return

    classifier.fit(X_train, y_train)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    save_model_path = save_model_with_timestamp(
        save_model_path, classifier_type, timestamp
    )
    print(save_model_path)
    save_tree_path = save_tree_with_timestamp(
        save_tree_path, classifier_type, timestamp
    )
    print(save_tree_path)
    log_file_path = save_log_model(
        SAVE_LOG_PATH,
        timestamp,
        classifier_type,
        len(X_train),
        len(X_test),
        classifier.get_params(),
    )
    print(log_file_path)
    evaluate_performance(classifier, X_train, y_train, X_test, y_test, log_file_path)
    joblib.dump(classifier, save_model_path)
    visualize_tree(classifier, classifier_type, FEATURES, save_tree_path)
