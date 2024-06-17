from src.cancer_diagnosis.training import train_evaluate_visualize_decision_tree
from src.connect_database.load_data import X, Y


def main():
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
            train_evaluate_visualize_decision_tree(X, Y, classifier_type="DecisionTree")
            print("----- ----- -----")
        elif choice == "2":
            print("Train RandomForest")
            train_evaluate_visualize_decision_tree(X, Y, classifier_type="RandomForest")
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


if __name__ == "__main__":
    main()
