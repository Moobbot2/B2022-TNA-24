import numpy as np
from src.cancer_diagnosis.training import train_evaluate_visualize_decision_tree
from src.connect_database.load_data import X, Y


def validate_data(X, Y):
    """
    Validate the consistency and format of X and Y.
    Convert them to NumPy arrays if necessary.
    """
    # Convert to NumPy arrays if not already
    if not isinstance(X, np.ndarray):
        X = np.array(X)
    if not isinstance(Y, np.ndarray):
        Y = np.array(Y)

    # Ensure X is 2D and Y is 1D
    if len(X.shape) == 1:
        X = X.reshape(-1, 1)  # Reshape to 2D
    if len(Y.shape) > 1:
        Y = Y.ravel()  # Flatten to 1D

    # Check that the number of samples matches
    assert len(X) == len(Y), "X and Y must have the same number of samples!"

    return X, Y


def main():
    """
    Main function for training models interactively.
    """
    try:
        # Validate the data before proceeding
        X_validated, Y_validated = validate_data(X, Y)
        print("Data validated successfully.")

        while True:
            print("===== $$$ =====")
            print("\nChoose an option:")
            print("1. Train DecisionTree")
            print("2. Train RandomForest")
            print("3. Train XGBoost")
            print("4. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                print("Train DecisionTree")
                train_evaluate_visualize_decision_tree(
                    X, Y, classifier_type="DecisionTree"
                )
                print("----- ----- -----")
            elif choice == "2":
                print("Train RandomForest")
                train_evaluate_visualize_decision_tree(
                    X, Y, classifier_type="RandomForest"
                )
                print("----- ----- -----")
            elif choice == "3":
                print("Train XGBoost")
                train_evaluate_visualize_decision_tree(X, Y, classifier_type="XGBoost")
                print("----- ----- -----")
            elif choice == "4":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please enter a valid option.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
