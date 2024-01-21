

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
import joblib
from config import FEATURES, KQ, OUTPUT_LINK
from model_CART import CARTNode

df = pd.read_excel(OUTPUT_LINK)

X = df[FEATURES]
y = df[KQ]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Example usage
# Assuming X_train and y_train are your training data and labels
dtree = CARTNode()
dtree.fit(X_train.values, y_train.values, max_depth=5)

# Make predictions on the training data
# y_train_pred = dtree.predict(X_train.values)
# # Evaluate the performance on the training data
# print("\nTraining Performance:")
# print("Accuracy:", accuracy_score(y_train, y_train_pred))
# print("Precision:", precision_score(y_train, y_train_pred, average='weighted'))
# print("Recall:", recall_score(y_train, y_train_pred, average='weighted'))
# print("F1 Score:", f1_score(y_train, y_train_pred, average='weighted'))
# print('--------------------------')

# y_test_pred = dtree.predict(X_test.values)
# print("\Test Performance:")
# print("Accuracy:", accuracy_score(y_test, y_test_pred))
# print("Precision:", precision_score(y_test, y_test_pred, average='weighted'))
# print("Recall:", recall_score(y_test, y_test_pred, average='weighted'))
# print("F1 Score:", f1_score(y_test, y_test_pred, average='weighted'))

# joblib.dump(dtree, 'model/cart_tree_model.joblib')
# fig = plt.figure(figsize=(150, 80))
# _ = tree.plot_tree(dtree, feature_names=FEATURES, filled=True)
# fig.savefig("model/cart_tree.png")
# Assuming 'classes' is a list of your class names
classes = sorted(df[KQ].unique())  # Adjust this based on your dataset
dtree.visualize_tree(FEATURES, sorted(df[KQ].unique()), 'custom_tree')
