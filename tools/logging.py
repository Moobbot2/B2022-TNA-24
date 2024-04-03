import os


def save_log_model(
    log_directory,
    timestamp,
    model_type,
    train_samples,
    test_samples,
    hyperparameters,
):
    log_file_name = f"log_{model_type}_{timestamp}.txt"
    log_file_path = os.path.join(log_directory, log_file_name)
    with open(log_file_path, "a") as f:
        f.write(f"Model Type: {model_type}\n")
        f.write(f"Training Samples: {train_samples}\n")
        f.write(f"Test Samples: {test_samples}\n")
        f.write("Hyperparameters:\n")
        for key, value in hyperparameters.items():
            f.write(f"{key}: {value}\n")
        f.write("--------------------------\n")
    return log_file_path
