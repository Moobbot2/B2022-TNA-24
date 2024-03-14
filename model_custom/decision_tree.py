import pandas as pd
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
import joblib
from config import FEATURES
from datasets import X, Y

# Create and train the decision tree model
dtree = DecisionTreeClassifier()
dtree = dtree.fit(X, Y)

# Get feature importance
feature_importance = dtree.feature_importances_

# Specify the encoding when opening the log file
log_file_path = 'decision_tree_feature_importance.log'
with open(log_file_path, 'w', encoding='utf-8') as log_file:
    for i, feature in enumerate(FEATURES):
        # Encode the feature name to handle non-ASCII characters
        encoded_feature = feature.encode('utf-8')
        log_file.write(
            f"{encoded_feature.decode('utf-8')}: {feature_importance[i]}\n")

# Save the model to a file
joblib.dump(dtree, 'decision_tree_model.joblib')

# Load the model later if needed
loaded_model = joblib.load('decision_tree_model.joblib')

# Visualize and save the decision tree
fig = plt.figure(figsize=(150, 80))
_ = tree.plot_tree(dtree, feature_names=FEATURES, filled=True)
fig.savefig("decision_tree.png")
