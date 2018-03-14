# File: tester.py 
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen
# Created: 06/03/2018
import ast;
from constants import *;
import numpy as np;
from sklearn.linear_model import LogisticRegression;
from sklearn.linear_model import RidgeClassifier;
from sklearn.dummy import DummyClassifier;

TRAIN_EPS_NUM = 20;
TEST_EPS_NUM = 10;

train_data_vec = [];

# go through all training episodes
for ep_num in range(1, TRAIN_EPS_NUM + 1):
    print('Getting vectors for training episode: ' + str(ep_num) + '/' + \
        str(TRAIN_EPS_NUM));
    vector_strs = [];
    with open(VECTORS_FOLDER + (EP_NUMBER_FORMAT % ep_num), 'r') as file:
        vector_strs = file.read().splitlines();

    for vector_str in vector_strs:
        train_data_vec.append(ast.literal_eval(vector_str));

train_data = np.array(train_data_vec);

train_data_vecs = train_data[:, :-1];
train_data_labels = train_data[:, -1];

test_data_vec = [];

# go through all testing episodes
for ep_num in range(TRAIN_EPS_NUM + 1, (TRAIN_EPS_NUM + 1) + TEST_EPS_NUM):
    print('Getting vectors for testing episode: ' + str(ep_num) + '/' + \
        str(TRAIN_EPS_NUM + TEST_EPS_NUM));
    vector_strs = [];
    with open(VECTORS_FOLDER + (EP_NUMBER_FORMAT % ep_num), 'r') as file:
        vector_strs = file.read().splitlines();

    for vector_str in vector_strs:
        test_data_vec.append(ast.literal_eval(vector_str));

test_data = np.array(test_data_vec);

test_data_vecs = test_data[:, :-1];
test_data_labels = test_data[:, -1];

# set up logistic regression classifier and fit to data
log_reg_clf = LogisticRegression(solver='newton-cg', max_iter=50,\
    random_state=0, multi_class='multinomial',\
    verbose=0).fit(train_data_vecs, train_data_labels);

print('Logistic Regression Accuracy: ' + \
    str(log_reg_clf.score(test_data_vecs, test_data_labels)));

ridge_clf = RidgeClassifier(solver='auto');
ridge_clf.fit(train_data_vecs, train_data_labels);

print('Ridge Regression Accuracy: ' + \
    str(ridge_clf.score(test_data_vecs, test_data_labels)));

dummy_clf = DummyClassifier(strategy='stratified');
dummy_clf.fit(train_data_vecs, train_data_labels);
print('Stratified Random Accuracy: ' + \
    str(dummy_clf.score(test_data_vecs, test_data_labels)));
