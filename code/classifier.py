# File: classifier.py 
# Author(s): Rishikesh Vaishnav, Jessica Lacovelli, Bonnie Chen

# Created: 06/02/2018
import numpy as np;
from constants import *;
from sklearn.linear_model import LogisticRegression;
from sklearn.neighbors import KNeighborsClassifier;
from sklearn.neural_network import MLPClassifier;
from sklearn.naive_bayes import MultinomialNB;
from sklearn.svm import SVC;

# load the raw data
filedata = None;
with open(RAW_TEXT_FILE, 'r') as file :
  filedata = file.read();

# open data file
with open(TRAINING_DATA_SELF_FILE, 'r') as f:
    data_text_raw = f.read().splitlines();

# numerical assignments of labels
label_nums = { 'pokemon': 0, 'person': 1, 'settlement': 2, 'move': 3,\
        'event':4, 'item': 5, 'region': 6, 'concept': 7, 'building':8,\
        'group':9, 'type': 10, 'condition':11};

# get length of vector
vector_size = int(data_text_raw[0]);

num_data = len(data_text_raw) - 1;

data = np.zeros((num_data, vector_size + 1));

# go through all lines in training data file
for i in range(1, len(data_text_raw)-1):
    items = data_text_raw[i].split('\t');
    label = label_nums[items[1]];
    vector_string = items[2];
    vector = [int(x) for x in vector_string.split()];
    vector.append(label);
    data[i, :] = vector;

vectors = data[:, :-1];
labels = data[:, -1];

num_training = int(TRAINING_SET_PROP * num_data);
print("num_training:" + str(num_training));

training_vectors = vectors[:(num_training + 1), :];
training_labels = labels[:(num_training + 1)];

test_vectors = vectors[(num_training + 1):, :];
test_labels = labels[(num_training + 1):];

#clf = LogisticRegression(solver='newton-cg', C=1000000, max_iter=1000, random_state=0, \
#    multi_class='multinomial', verbose=1).fit(training_vectors, \
#    training_labels);
#
#print('Logistic regression result:', clf.score(test_vectors, test_labels));

clf = KNeighborsClassifier(n_neighbors=50);
clf.fit(training_vectors, training_labels);

print('K nearest neighbors result:',clf.score(test_vectors, test_labels));
#
#clf = MLPClassifier(solver='lbfgs', alpha=1e-5, \
#        hidden_layer_sizes=(5, 2), random_state=1)
#
#clf.fit(training_data_predictors, training_data_labels);
#
#print('Multilayer perceptron result:',clf.score(unclassified_data, unclassified_data_labels));
#
#clf = MultinomialNB();
#
#clf.fit(training_data_predictors, training_data_labels);
#
#print('Multinomial naive bayes result:',clf.score(unclassified_data, unclassified_data_labels));
#
#clf = SVC(degree=1, kernel='poly', verbose=False);
#
#clf.fit(training_data_predictors, training_data_labels);
#
#print('Support vector machine result:',clf.score(unclassified_data, unclassified_data_labels));
