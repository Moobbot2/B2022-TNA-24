import program
from datasets import X, Y

print('Train DecisionTree')
program.train_evaluate_visualize_decision_tree(
    X, Y, classifier_type='DecisionTree')
print('----- ----- -----')

# print('Train RandomForest')
# program.train_evaluate_visualize_decision_tree(
#     X, Y, classifier_type='RandomForest', save_model_path='output/model/random_forest_model.joblib')
# print('----- ----- -----')

# print('Train XGBoost')
# program.train_evaluate_visualize_decision_tree(
#     X, Y, classifier_type='XGBoost', save_model_path='output/model/xgboost_model.joblib')
