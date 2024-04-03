from config.config import (
    DB_HOST,
    DB_NAME,
    DB_PASSWORD,
    DB_USERNAME,
    FEATURES,
    KQ,
    TABLE_NAME,
)
from src.cancer_diagnosis.training import train_evaluate_visualize_decision_tree
from src.connect_database import database_utils
from tools.utils import create_dataframe_from_table_data

mydb = database_utils.connect_to_database(
    db_host=DB_HOST,
    db_name=DB_NAME,
    db_username=DB_USERNAME,
    db_password=DB_PASSWORD,
)
column_names = FEATURES + [KQ]
data_table = database_utils.fetch_data_from_table(mydb, TABLE_NAME)
df = create_dataframe_from_table_data(data_table, column_names)
X = df[FEATURES]
Y = df[KQ]
print("Train DecisionTree")
train_evaluate_visualize_decision_tree(X, Y, classifier_type="DecisionTree")
print("----- ----- -----")

print("Train RandomForest")
train_evaluate_visualize_decision_tree(X, Y, classifier_type="RandomForest")
print("----- ----- -----")

print("Train XGBoost")
train_evaluate_visualize_decision_tree(X, Y, classifier_type="XGBoost")
