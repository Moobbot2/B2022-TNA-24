import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Assuming you have the dataset in a xlsx file named 'hello.xlsx'
df = pd.read_excel("hello.xlsx")

# Assuming the target variable is named 'KQ' (1 for cancer, 0 for no cancer)
features = ["đau bụng", "nôn", "chán ăn", "táo bón", "sút cân",
            "tiêu chảy", "phân có máu", "da niêm mạc vàng", "da sạm", 
            "hoạch ngoại biên", "hạch thượng đòn", 
            "bụng chướng", "phản ứng thành bụng", "cảm ứng phúc mạc", 
            "dấu hiệu rắn bò", "quai ruột nổi", 
            "sờ thấy khối u", "thăm trực tràng có khối u", "tiền sử ung thư",
            "chụp CT ổ bụng có khối u", "nội soi đại tràng có khối u"]

X = df[features]
y = df['KQ']

# Create a new data point for prediction
new_data_point = pd.DataFrame([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                               columns=features)

# Split the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Load the decision tree model
loaded_model = joblib.load('decision_tree_model.joblib')

print(new_data_point)
# Make predictions on the testing data
y_pred = loaded_model.predict(new_data_point)
print("Prediction:", y_pred)
# Evaluate the accuracy of the model
# accuracy = accuracy_score(y_test, y_pred)
# print(f"Model Accuracy: {accuracy}")
