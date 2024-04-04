import pandas as pd
from unidecode import unidecode


try:
    from config.config import (FEATURES, KQ)
    from src.cancer_diagnosis.training import train_evaluate_visualize_decision_tree
except:
    from helpers import add_path_init
    add_path_init()
    from config import (FEATURES, KQ)
    from cancer_diagnosis.training import train_evaluate_visualize_decision_tree

excel_file = "./dataset/datatest.xlsx"
df = pd.read_excel(excel_file)
# print(df)

for col in df.columns:
    new_col = unidecode(col).replace(" ", "_")
    df.rename(columns={col: new_col}, inplace=True)

print(df)
X = df[FEATURES]
Y = df[KQ]

print(X)
print(Y)

train_evaluate_visualize_decision_tree(X, Y, classifier_type="DecisionTree")
