import program
from datasets import X, Y

print('Train DecisionTree')
program.train_evaluate_visualize_decision_tree(
    X, Y, classifier_type='DecisionTree')
print('----- ----- -----')

print('Train RandomForest')
program.train_evaluate_visualize_decision_tree(
    X, Y, classifier_type='RandomForest')
print('----- ----- -----')

print('Train XGBoost')
program.train_evaluate_visualize_decision_tree(
    X, Y, classifier_type='XGBoost')
