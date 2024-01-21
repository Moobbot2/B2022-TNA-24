import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
from config import FEATURES, KQ, OUTPUT_LINK


class CARTNode:
    def __init__(self, depth=0, max_depth=None):
        self.feature_index = None
        self.threshold = None
        self.left = None
        self.right = None
        self.value = None
        self.depth = depth
        self.max_depth = max_depth

    def _calculate_gini(self, y):
        _, counts = np.unique(y, return_counts=True)
        probabilities = counts / len(y)
        gini = 1 - np.sum(probabilities**2)
        return gini

    def _split_data(self, X, y, feature_index, threshold):
        left_mask = X[:, feature_index] <= threshold
        right_mask = ~left_mask
        return X[left_mask], y[left_mask], X[right_mask], y[right_mask]

    def _find_best_split(self, X, y):
        m, n = X.shape
        if m <= 1:
            return None, None

        gini_parent = self._calculate_gini(y)

        best_gini = 1
        best_feature = None
        best_threshold = None

        for feature_index in range(n):
            thresholds = np.unique(X[:, feature_index])
            for threshold in thresholds:
                X_left, y_left, X_right, y_right = self._split_data(
                    X, y, feature_index, threshold)

                if len(y_left) == 0 or len(y_right) == 0:
                    continue

                gini_left = self._calculate_gini(y_left)
                gini_right = self._calculate_gini(y_right)

                gini_split = (len(y_left) / m) * gini_left + \
                    (len(y_right) / m) * gini_right

                if gini_split < best_gini:
                    best_gini = gini_split
                    best_feature = feature_index
                    best_threshold = threshold

        return best_feature, best_threshold

    def _build_tree(self, X, y):
        if self.depth == self.max_depth or np.all(y == y[0]):
            self.value = np.argmax(np.bincount(y))
            return

        feature, threshold = self._find_best_split(X, y)

        if feature is None:
            self.value = np.argmax(np.bincount(y))
            return

        self.feature_index = feature
        self.threshold = threshold

        X_left, y_left, X_right, y_right = self._split_data(
            X, y, feature, threshold)

        self.left = CARTNode(depth=self.depth + 1, max_depth=self.max_depth)
        self.left._build_tree(X_left, y_left)

        self.right = CARTNode(depth=self.depth + 1, max_depth=self.max_depth)
        self.right._build_tree(X_right, y_right)

    def fit(self, X, y, max_depth=None):
        self.max_depth = max_depth
        self._build_tree(X, y)

    def predict_sample(self, sample):
        if self.value is not None:
            return self.value

        if sample[self.feature_index] <= self.threshold:
            return self.left.predict_sample(sample)
        else:
            return self.right.predict_sample(sample)

    def predict(self, X):
        return np.array([self.predict_sample(sample) for sample in X])


df = pd.read_excel(OUTPUT_LINK)

X = df[FEATURES]
y = df[KQ]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Example usage
# Assuming X_train and y_train are your training data and labels
tree = CARTNode()
tree.fit(X_train.values, y_train.values, max_depth=5)

# Make predictions on the training data
y_train_pred = tree.predict(X_train.values)
# Evaluate the performance on the training data
print("\nTraining Performance:")
print("Accuracy:", accuracy_score(y_train, y_train_pred))
print("Precision:", precision_score(y_train, y_train_pred, average='weighted'))
print("Recall:", recall_score(y_train, y_train_pred, average='weighted'))
print("F1 Score:", f1_score(y_train, y_train_pred, average='weighted'))
print('--------------------------')

y_test_pred = tree.predict(X_test.values)
print("\Test Performance:")
print("Accuracy:", accuracy_score(y_test, y_test_pred))
print("Precision:", precision_score(y_test, y_test_pred, average='weighted'))
print("Recall:", recall_score(y_test, y_test_pred, average='weighted'))
print("F1 Score:", f1_score(y_test, y_test_pred, average='weighted'))
