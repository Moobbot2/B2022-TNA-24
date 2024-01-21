import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
from config import FEATURES, KQ, OUTPUT_LINK
# Assuming you have the dataset in a xlsx file named 'hello.xlsx'
df = pd.read_excel(OUTPUT_LINK)

X = df[FEATURES]
y = df[KQ]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)


# Load the decision tree model
loaded_model = joblib.load('./model/cart_tree_model.joblib')

# Make predictions on the testing data
y_train_pred = loaded_model.predict(X_train.values)
y_test_pred = loaded_model.predict(X_test.values)
print("\nTraining Performance:")
print("Accuracy:", accuracy_score(y_train, y_train_pred))
print("Precision:", precision_score(y_train, y_train_pred, average='weighted'))
print("Recall:", recall_score(y_train, y_train_pred, average='weighted'))
print("F1 Score:", f1_score(y_train, y_train_pred, average='weighted'))
print('--------------------------')
print("\Test Performance:")
print("Accuracy:", accuracy_score(y_test, y_test_pred))
print("Precision:", precision_score(y_test, y_test_pred, average='weighted'))
print("Recall:", recall_score(y_test, y_test_pred, average='weighted'))
print("F1 Score:", f1_score(y_test, y_test_pred, average='weighted'))
