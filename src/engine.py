from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
from model_CART import CARTNode
from config import FEATURES
from datasets import X, Y

# Chia dữ liệu thành tập huấn luyện và tập kiểm thử
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)


dtree = CARTNode()
dtree.fit(X_train.values, y_train.values, max_depth=5)

y_train_pred = dtree.predict(X_train.values)

print("\nTraining Performance:")
print("Accuracy:", accuracy_score(y_train, y_train_pred))
print("Precision:", precision_score(y_train, y_train_pred, average='weighted'))
print("Recall:", recall_score(y_train, y_train_pred, average='weighted'))
print("F1 Score:", f1_score(y_train, y_train_pred, average='weighted'))
print('--------------------------')

y_test_pred = dtree.predict(X_test.values)
print("\Test Performance:")
print("Accuracy:", accuracy_score(y_test, y_test_pred))
print("Precision:", precision_score(y_test, y_test_pred, average='weighted'))
print("Recall:", recall_score(y_test, y_test_pred, average='weighted'))
print("F1 Score:", f1_score(y_test, y_test_pred, average='weighted'))

joblib.dump(dtree, 'model/cart_tree_model.joblib')
classes = sorted(Y.unique()) 
dtree.visualize_tree(FEATURES, classes, 'model/cart_tree')
