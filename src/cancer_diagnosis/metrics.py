import time

from tools.metrics import log_metrics, performance_calculation
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def metrics_performance(classifier, X, y_true):
    start_time = time.time()
    y_pred = classifier.predict(X)
    end_time = time.time()
    elapsed_time = end_time - start_time
    accuracy, precision, recall, f1 = performance_calculation(y_true, y_pred)
    return accuracy, precision, recall, f1, elapsed_time


def evaluate_performance(classifier, X_train, y_train, X_test, y_test, log_file_path):
    train_metrics = metrics_performance(classifier, X_train, y_train)
    test_metrics = metrics_performance(classifier, X_test, y_test)
    log_metrics(train_metrics, test_metrics, log_file_path)
