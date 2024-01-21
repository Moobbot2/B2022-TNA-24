import xgboost as xgb
from xgboost import plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("./dataset/output.xlsx")

features = ["đau bụng", "nôn", "chán ăn", "táo bón", "sút cân",
            "tiêu chảy", "phân có máu", "da niêm mạc vàng", "da sạm",
            "hoạch ngoại biên", "hạch thượng đòn",
            "bụng chướng", "phản ứng thành bụng", "cảm ứng phúc mạc",
            "dấu hiệu rắn bò", "quai ruột nổi",
            "sờ thấy khối u", "thăm trực tràng có khối u", "tiền sử ung thư",
            "chụp CT ổ bụng có khối u", "nội soi đại tràng có khối u"]

X = df[features]
y = df['KQ']

# Tách dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

# Tạo mô hình XGBoost
xgb_model = xgb.XGBClassifier(objective='binary:logistic', random_state=42)

# Huấn luyện mô hình
xgb_model.fit(X_train, y_train)

# Dự đoán trên tập kiểm tra
y_pred = xgb_model.predict(X_test)

# Đánh giá mô hình
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print(f'Accuracy: {accuracy:.4f}')
print(f'Precision: {precision:.4f}')
print(f'Recall: {recall:.4f}')
print(f'F1 Score: {f1:.4f}')

# Lưu mô hình vào file
xgb_model.save_model('output_tree/xgb_model_6_4.model')

# # Đặt kích thước của hình hiển thị
# plt.figure(figsize=(20, 10))
# # Lưu cây quyết định vào file DOT
# plot_tree(xgb_model, num_trees=0, ax=plt.gca())# num_trees là số cây muốn vẽ (0 là cây đầu tiên)
# plt.show()
# # Lưu hình ảnh vào file
# plt.savefig('output_tree/xgboost_tree_8_2.png')