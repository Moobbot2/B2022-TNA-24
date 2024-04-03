import numpy as np
from graphviz import Digraph
import matplotlib.pyplot as plt


class CARTNode:
    """
    feature_index: chỉ số của thuộc tính sử dụng để chia
    threshold: ngưỡng chia
    left và right: tham chiếu tới nút con trái và phải
    value: giá trị dự đoán tại nút
    depth: độ sâu của nút trong cây
    max_depth: độ sâu tối đa của cây

    _calculate_gini: phương thức tính chỉ số Gini impurity cho một tập dữ liệu mục tiêu y
    _split_data: phương thức chia tập dữ liệu X và nhãn tương ứng y dựa trên một thuộc tính và ngưỡng cụ thể.
    _find_best_split: phương thức duyệt qua tất cả các thuộc tính và các giá trị duy nhất của chúng để tìm ra cặp thuộc tính
    và ngưỡng tốt nhất để chia giảm Gini impurity.
    _build_tree: phương thức xây dựng cây quyết định một cách đệ quy bằng cách tìm kiếm chia tốt nhất tại mỗi nút và tạo các nút con.
    fit: khởi động quá trình xây dựng cây bằng cách gọi _build_tree với dữ liệu huấn luyện.
    predict_sample: phương thức thực hiện dự đoán cho một mẫu đơn bằng cách đi qua cây dựa trên giá trị của các thuộc tính.
    predict: phương thức thực hiện dự đoán cho toàn bộ tập dữ liệu X bằng cách áp dụng predict_sample cho từng mẫu.
    """

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
        m, n = X.shape  # Lấy số hàng (m) và số cột (n) của ma trận X.
        # Nếu số mẫu trong tập dữ liệu là 1 hoặc ít hơn, không thể thực hiện phân chia, trả về None, None.
        if m <= 1:
            return None, None

        gini_parent = self._calculate_gini(y)

        best_gini = 1  # Khởi tạo giá trị Gini impurity tốt nhất ban đầu là 1
        best_feature = None  # Khởi tạo chỉ số của thuộc tính tốt nhất
        best_threshold = None  # Khởi tạo giá trị ngưỡng tốt nhất

        # Duyệt qua tất cả các thuộc tính trong tập dữ liệu.
        for feature_index in range(n):
            # Lấy các giá trị duy nhất của thuộc tính hiện tại.
            thresholds = np.unique(X[:, feature_index])
            for threshold in thresholds:
                # Tạo các tập dữ liệu con bằng cách chia dữ liệu chính thành hai phần dựa trên giá trị ngưỡng và thuộc tính hiện tại.
                X_left, y_left, X_right, y_right = self._split_data(
                    X, y, feature_index, threshold)
                # Nếu một trong hai tập dữ liệu con không có mẫu, bỏ qua và tiếp tục vòng lặp.
                if len(y_left) == 0 or len(y_right) == 0:
                    continue

                # Tính Gini impurity cho tập dữ liệu con trái/phải
                gini_left = self._calculate_gini(y_left)
                gini_right = self._calculate_gini(y_right)
                # Tính Gini impurity sau khi chia dữ liệu và tính trọng số dựa trên số lượng mẫu trong mỗi tập dữ liệu con.
                gini_split = (len(y_left) / m) * gini_left + \
                    (len(y_right) / m) * gini_right

                # Nếu Gini impurity sau khi chia nhỏ hơn Gini impurity tốt nhất hiện tại, cập nhật giá trị tốt nhất và chỉ số thuộc tính, ngưỡng.
                if gini_split < best_gini:
                    best_gini = gini_split
                    best_feature = feature_index
                    best_threshold = threshold
        # Trả về thuộc tính và giá trị ngưỡng tốt nhất sau khi duyệt qua tất cả các giá trị và thuộc tính.
        return best_feature, best_threshold

    def _build_tree(self, X, y):
        # Kiểm tra điều kiện dừng xây dựng cây.
        # Nếu độ sâu của nút bằng độ sâu tối đahoặc tất cả các nhãn trong tập dữ liệu là giống nhau,
        # dừng xây dựng cây và gán giá trị dự đoán cho nút (self.value) là nhãn xuất hiện nhiều nhất.
        if self.depth == self.max_depth or np.all(y == y[0]):
            self.value = np.argmax(np.bincount(y))
            # Calculate Gini impurity for leaf nodes
            self.gini = self._calculate_gini(y)
            return
        #  Tìm ra cặp thuộc tính và ngưỡng tối ưu để chia tập dữ liệu.
        feature, threshold = self._find_best_split(X, y)

        if feature is None:
            self.value = np.argmax(np.bincount(y))
            # Calculate Gini impurity for leaf nodes
            self.gini = self._calculate_gini(y)
            return

        self.feature_index = feature  # Gán chỉ số của thuộc tính cho nút.
        self.threshold = threshold  # Gán giá trị ngưỡng cho nút.

        X_left, y_left, X_right, y_right = self._split_data(
            X, y, feature, threshold)

        self.left = CARTNode(depth=self.depth + 1, max_depth=self.max_depth)
        self.left._build_tree(X_left, y_left)

        self.right = CARTNode(depth=self.depth + 1, max_depth=self.max_depth)
        self.right._build_tree(X_right, y_right)

        # Calculate Gini impurity for non-leaf nodes
        self.gini = self._calculate_gini(y)

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

    def visualize_tree_graphviz(self, feature_names, class_names, file_name='tree'):
        dot = Digraph(comment='Decision Tree')

        def add_node(node, parent_name=None, edge_label=None):
            if node.feature_index is not None:
                feature_name = feature_names[node.feature_index]
                label = f'{feature_name} <= {node.threshold:.2f}\nGini: {node.gini:.2f}'
            else:
                label = f'Class {class_names[node.value]}\nGini: {node.gini:.2f}'

            dot.node(str(id(node)), label=label)

            if parent_name is not None:
                dot.edge(parent_name, str(id(node)), label=edge_label)

            if node.left is not None:
                add_node(node.left, str(id(node)), 'True')
            if node.right is not None:
                add_node(node.right, str(id(node)), 'False')

        add_node(self)

        # Save the tree visualization as a PNG file
        dot.render(file_name, format='png', cleanup=True)

    def visualize_tree_txt(self, feature_names, class_names, file_name='tree.txt'):
        def write_tree(node, file, indent=''):
            if node.feature_index is not None:
                feature_name = feature_names[node.feature_index]
                file.write(
                    f"{indent}if {feature_name} <= {node.threshold:.2f}:\n")
            else:
                file.write(f"{indent}return Class {class_names[node.value]}\n")

            if node.left is not None:
                write_tree(node.left, file, indent + '  ')
            if node.right is not None:
                write_tree(node.right, file, indent + '  ')

        with open(file_name, 'w', encoding='utf-8') as file:  # Specify encoding as 'utf-8'
            write_tree(self, file)
