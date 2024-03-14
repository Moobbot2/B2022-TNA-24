import joblib
import xgboost
from xgboost import plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
from datasets import X, Y

# Chia dữ liệu thành tập huấn luyện và tập kiểm thử
X_train, X_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.2, random_state=42)

# Tạo mô hình XGBoost
xgb_model = xgboost.XGBClassifier(objective='binary:logistic', random_state=42)

# Huấn luyện mô hình
xgb_model.fit(X_train, y_train)

# Dự đoán trên tập kiểm thử
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
# xgb_model.save_model('model/xgboost_tree_8_2.json')
joblib.dump(xgb_model, 'model/xgboost_model.joblib')

# # Đặt kích thước của hình hiển thị
plt.figure(figsize=(20, 10))
# Lưu cây quyết định vào file DOT
plot_tree(xgb_model, num_trees=0, ax=plt.gca())  # num_trees cây muốn vẽ thứ n
# Lưu hình ảnh vào file
plt.savefig('model/xgboost_tree_8_2.png')
plt.show()
