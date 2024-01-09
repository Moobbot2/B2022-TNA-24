from sklearn.tree import DecisionTreeClassifier
import joblib

# Load the decision tree model
loaded_model = joblib.load('decision_tree_model.joblib')

# Assuming you have a new data point for prediction
new_data_point = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]  # Replace this with your actual data

# Set the feature names for the loaded model
loaded_model.feature_names = ["đau bụng", "nôn", "chán ăn", "táo bón", "sút cân",
                              "tiêu chảy", "phân có máu", "da niêm mạc vàng", "da sạm", 
                              "hoạch ngoại biên", "hạch thượng đòn", 
                              "bụng chướng", "phản ứng thành bụng", "cảm ứng phúc mạc", 
                              "dấu hiệu rắn bò", "quai ruột nổi", 
                              "sờ thấy khối u", "thăm trực tràng có khối u", "tiền sử ung thư",
                              "chụp CT ổ bụng có khối u", "nội soi đại tràng có khối u"]

# Make predictions using the loaded model
predictions = loaded_model.predict(new_data_point)

print("Predictions:", predictions)
