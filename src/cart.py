import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pandas as pd
import matplotlib.pyplot as plt

class Node:
    def __init__(self, data, target):
        self.data = data
        self.target = target
        self.left = None
        self.right = None
        self.feature_index = None
        self.threshold = None
        self.prediction = None


def gini_index(groups, classes):
    total_instances = float(sum(len(group) for group in groups))
    gini = 0.0
    for group in groups:
        size = float(len(group))
        if size == 0:
            continue
        score = 0.0
        for class_val in classes:
            p = [row[-1] for row in group].count(class_val) / size
            score += p * p
        gini += (1.0 - score) * (size / total_instances)
    return gini


def test_split(index, value, data):
    left, right = list(), list()
    for row in data:
        if row[index] < value:
            left.append(row)
        else:
            right.append(row)
    return left, right


def get_split(data):
    class_values = list(set(row[-1] for row in data))
    b_index, b_value, b_score, b_groups = float(
        'inf'), float('inf'), float('inf'), None
    for index in range(len(data[0])-1):
        for row in data:
            groups = test_split(index, row[index], data)
            gini = gini_index(groups, class_values)
            if gini < b_score:
                b_index, b_value, b_score, b_groups = index, row[index], gini, groups
    return {'index': b_index, 'value': b_value, 'groups': b_groups}


def to_terminal(group):
    outcomes = [row[-1] for row in group]
    return max(set(outcomes), key=outcomes.count)


def split(node, max_depth, min_size, depth):
    left, right = node['groups']
    del (node['groups'])
    if not left or not right:
        node['left'] = node['right'] = to_terminal(left + right)
        return
    if depth >= max_depth:
        node['left'], node['right'] = to_terminal(left), to_terminal(right)
        return
    if len(left) <= min_size:
        node['left'] = to_terminal(left)
    else:
        node['left'] = get_split(left)
        split(node['left'], max_depth, min_size, depth+1)
    if len(right) <= min_size:
        node['right'] = to_terminal(right)
    else:
        node['right'] = get_split(right)
        split(node['right'], max_depth, min_size, depth+1)


def build_tree(train, max_depth, min_size):
    root = get_split(train)
    split(root, max_depth, min_size, 1)
    return root


def print_tree(node, depth=0):
    if isinstance(node, dict):
        print('{}[X{} < {}]'.format(depth*' ', node['index'], node['value']))
        print_tree(node['left'], depth+1)
        print_tree(node['right'], depth+1)
    else:
        print('{}[{}]'.format(depth*' ', node))

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
# Example usage:
# Assuming your data is in the format: [[feature1, feature2, ..., target], ...]
data = np.array([[2.771244718, 1.784783929, 0],
                 [1.728571309, 1.169761413, 0],
                 [3.678319846, 2.81281357, 0],
                 [3.961043357, 2.61995032, 0],
                 [2.999208922, 2.209014212, 0],
                 [7.497545867, 3.162953546, 1],
                 [9.00220326, 3.339047188, 1],
                 [7.444542326, 0.476683375, 1],
                 [10.12493903, 3.234550982, 1],
                 [6.642287351, 3.319983761, 1]])

tree = build_tree(data, max_depth=3, min_size=1)
print_tree(tree)