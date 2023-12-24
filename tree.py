import pandas
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt

df = pandas.read_excel("hello.xlsx")
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

dtree = DecisionTreeClassifier()
dtree = dtree.fit(X, y)

fig = plt.figure(figsize=(75,50))
_ = tree.plot_tree(dtree, feature_names=features, filled=True)
fig.savefig("decistion_tree.png")

# Gini = 1 - (x/n)^2 - (y/n)^2
# print(dtree.predict([[40, 10, 6, 1]]))
