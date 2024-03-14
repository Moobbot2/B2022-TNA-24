import joblib
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
import datetime
from config import FEATURES, TEST_SIZE, RAMDOM_STATE, N_ESTIMATORS, SAVE_MODEL_PATH, SAVE_TREE_PATH, SAVE_LOG_PATH
import os
import time


def metrics_performance(classifier, X, y):
    start_time = time.time()
    y_pred = classifier.predict(X)
    end_time = time.time()
    elapsed_time = end_time - start_time

    accuracy = accuracy_score(y, y_pred)
    precision = precision_score(y, y_pred, average='weighted')
    recall = recall_score(y, y_pred, average='weighted')
    f1 = f1_score(y, y_pred, average='weighted')
    return accuracy, precision, recall, f1, elapsed_time


def evaluate_performance(classifier, X_train, y_train, X_test, y_test, log_file_path):
    train_metrics = metrics_performance(classifier, X_train, y_train)
    test_metrics = metrics_performance(classifier, X_test, y_test)
    with open(log_file_path, 'a') as f:
        f.write("\nTraining Performance:\n")
        f.write(f"Accuracy: {train_metrics[0]}\n")
        f.write(f"Precision: {train_metrics[1]}\n")
        f.write(f"Recall: {train_metrics[2]}\n")
        f.write(f"F1 Score: {train_metrics[3]}\n")
        f.write(f"Elapsed Time (s): {train_metrics[4]}\n")
        f.write('--------------------------\n')
        f.write("\nTest Performance:\n")
        f.write(f"Accuracy: {test_metrics[0]}\n")
        f.write(f"Precision: {test_metrics[1]}\n")
        f.write(f"Recall: {test_metrics[2]}\n")
        f.write(f"F1 Score: {test_metrics[3]}\n")
        f.write(f"Elapsed Time (s): {test_metrics[4]}\n")
        f.write('--------------------------\n')


def save_log_model(log_directory, timestamp, classifier_type, train_samples, test_samples, hyperparameters):
    log_file_name = f"log_{classifier_type}_{timestamp}.txt"
    log_file_path = os.path.join(log_directory, log_file_name)
    with open(log_file_path, 'a') as f:
        f.write(f"Model Type: {classifier_type}\n")
        f.write(f"Training Samples: {train_samples}\n")
        f.write(f"Test Samples: {test_samples}\n")
        f.write("Hyperparameters:\n")
        for key, value in hyperparameters.items():
            f.write(f"{key}: {value}\n")
        f.write('--------------------------\n')
    return log_file_path


def save_model_with_timestamp(save_model_path, classifier_type, timestamp):
    return os.path.join(save_model_path, f"{classifier_type}_{timestamp}.joblib")
    # return f"{save_model_path}/{classifier_type}_{timestamp}.joblib"


def save_tree_with_timestamp(save_tree_path, classifier_type, timestamp):
    return os.path.join(save_tree_path, f"{classifier_type}_{timestamp}.png")
    # return f"{save_tree_path}/{classifier_type}_{timestamp}.png"


def visualize_tree(classifier, classifier_type, save_tree_path=None):
    if classifier_type == 'DecisionTree' and save_tree_path:
        plt.figure(figsize=(120, 80))
        plot_tree(classifier, feature_names=FEATURES,
                  class_names=['1', '0'], filled=True)
        plt.savefig(save_tree_path)


def train_evaluate_visualize_decision_tree(x, y, classifier_type, save_model_path=SAVE_MODEL_PATH, save_tree_path=SAVE_TREE_PATH):
    if classifier_type == 'DecisionTree':
        classifier = DecisionTreeClassifier()
    elif classifier_type == 'RandomForest':
        classifier = RandomForestClassifier(
            n_estimators=N_ESTIMATORS, random_state=RAMDOM_STATE)
    elif classifier_type == 'XGBoost':
        classifier = xgb.XGBClassifier(
            objective='binary:logistic', random_state=RAMDOM_STATE)
    # Chia dữ liệu thành tập huấn luyện và tập kiểm thử
    X_train, X_test, y_train, y_test = train_test_split(
        x, y, test_size=TEST_SIZE, random_state=RAMDOM_STATE)
    classifier.fit(X_train, y_train)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    save_model_path = save_model_with_timestamp(
        save_model_path, classifier_type, timestamp)
    print(save_model_path)
    save_tree_path = save_tree_with_timestamp(
        save_tree_path, classifier_type, timestamp)
    print(save_tree_path)
    log_file_path = save_log_model(SAVE_LOG_PATH, timestamp, classifier_type, len(
        X_train), len(X_test), classifier.get_params())
    print(log_file_path)
    evaluate_performance(classifier, X_train, y_train,
                         X_test, y_test, log_file_path)
    joblib.dump(classifier, save_model_path)
    # visualize_tree(classifier, classifier_type, save_tree_path)
