import program
from datasets import X, Y
from config import SAVE_MODEL_PATH, SAVE_TREE_PATH

print('Train DecisionTree')
program.train_evaluate_visualize_decision_tree(X, Y, classifier_type='DecisionTree',
                                               save_model_path=SAVE_MODEL_PATH, save_tree_path=SAVE_TREE_PATH)
print('----- ----- -----')

# print('Train RandomForest')
# program.train_evaluate_visualize_decision_tree(
#     X, Y, classifier_type='RandomForest', save_model_path='output/model/random_forest_model.joblib')
# print('----- ----- -----')

# print('Train XGBoost')
# program.train_evaluate_visualize_decision_tree(
#     X, Y, classifier_type='XGBoost', save_model_path='output/model/xgboost_model.joblib')
