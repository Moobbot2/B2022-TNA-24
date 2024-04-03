from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import time


def performance_calculation(y_true, y_pred):
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average="weighted")
    recall = recall_score(y_true, y_pred, average="weighted")
    f1 = f1_score(y_true, y_pred, average="weighted")
    return accuracy, precision, recall, f1


def log_metrics(train_metrics, test_metrics, log_file_path):
    with open(log_file_path, "a") as f:
        f.write("\nTraining Performance:\n")
        f.write(f"Accuracy: {train_metrics[0]}\n")
        f.write(f"Precision: {train_metrics[1]}\n")
        f.write(f"Recall: {train_metrics[2]}\n")
        f.write(f"F1 Score: {train_metrics[3]}\n")
        f.write(f"Elapsed Time (s): {train_metrics[4]}\n")
        f.write("--------------------------\n")
        f.write("\nTest Performance:\n")
        f.write(f"Accuracy: {test_metrics[0]}\n")
        f.write(f"Precision: {test_metrics[1]}\n")
        f.write(f"Recall: {test_metrics[2]}\n")
        f.write(f"F1 Score: {test_metrics[3]}\n")
        f.write(f"Elapsed Time (s): {test_metrics[4]}\n")
        f.write("--------------------------\n")
