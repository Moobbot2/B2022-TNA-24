import pandas as pd
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
import joblib

df = pd.read_excel("hello.xlsx")
# print(df)

features = ["đau bụng", "nôn", "chán ăn", "táo bón", "sút cân",
            "tiêu chảy", "phân có máu", "da niêm mạc vàng", "da sạm",
            "hoạch ngoại biên", "hạch thượng đòn",
            "bụng chướng", "phản ứng thành bụng", "cảm ứng phúc mạc",
            "dấu hiệu rắn bò", "quai ruột nổi",
            "sờ thấy khối u", "thăm trực tràng có khối u", "tiền sử ung thư",
            "chụp CT ổ bụng có khối u", "nội soi đại tràng có khối u"]

X = df[features]
y = df['KQ']

# Create and train the decision tree model
dtree = DecisionTreeClassifier()
dtree = dtree.fit(X, y)

# Get feature importance
feature_importance = dtree.feature_importances_

# Specify the encoding when opening the log file
log_file_path = 'decision_tree_feature_importance.log'
with open(log_file_path, 'w', encoding='utf-8') as log_file:
    for i, feature in enumerate(features):
        # Encode the feature name to handle non-ASCII characters
        encoded_feature = feature.encode('utf-8')
        log_file.write(f"{encoded_feature.decode('utf-8')}: {feature_importance[i]}\n")



# Save the model to a file
joblib.dump(dtree, 'decision_tree_model.joblib')

# Load the model later if needed
loaded_model = joblib.load('decision_tree_model.joblib')

# Visualize and save the decision tree
fig = plt.figure(figsize=(150, 80))
_ = tree.plot_tree(dtree, feature_names=features, filled=True)
fig.savefig("decision_tree.png")

# Gini = 1 - (x/n)^2 - (y/n)^2
# print(dtree.predict([[40, 10, 6, 1]]))
