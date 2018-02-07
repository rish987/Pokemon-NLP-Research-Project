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

# should data be normalized?
normalize = True;

# load the raw data
filedata = None;
with open(RAW_TEXT_FILE, 'r') as file :
  filedata = file.read();

# open data file
with open(TRAINING_DATA_SELF_FILE, 'r') as f:
    data_text_raw = f.read().splitlines();

# to hold all descriptor objects
descriptors = [];

# numerical assignments of labels
label_nums = { 'pokemon': 0, 'person': 1, 'settlement': 2, 'move': 3,\
        'event':4, 'item': 5, 'region': 6, 'concept': 7, 'building':8,\
        'group':9, 'type': 10, 'condition':11};

descriptor_and_label_strings = [];
with open(RANDOM_LABELED_CORRECTED_DESCRIPTORS_FILE, 'r') as f:
    descriptor_and_label_strings = f.read().splitlines();

first_test_i = int(len(descriptor_and_label_strings) * TRAINING_SET_PROP);
num_training_data = first_test_i;
num_tests = 50;
last_test_i = first_test_i + num_tests;
#last_test_i = len(descriptor_and_label_strings);
num_test_data = last_test_i - first_test_i;
vector_size = len(POS_TERMS);

# go through last 80% of data
for i in range(first_test_i, last_test_i):
    descriptor_and_label_string = descriptor_and_label_strings[i];
    descriptor_and_label_split = descriptor_and_label_string.split('\t\t');
    descriptor_string = descriptor_and_label_split[1];
    label_string = descriptor_and_label_split[0];
    print("Processing descriptor " + str(i + 1) + "/" + str(last_test_i) + ": " + descriptor_string);
    # search for all matches to descriptor, and also grab surrounding words
    all_found = re.findall( regex % \
            re.escape(descriptor_string), filedata);
    descriptor = Descriptor(descriptor_string, label_string);
    if len(all_found) == 0:
        print("\tNO MATCH FOUND");

    for found in all_found:
        # pass the words on the the descriptor for it to add them to its
        # dictionary
        descriptor.add_words(found);

    descriptors.append(descriptor);

unclassified_data = np.zeros((num_test_data, vector_size));
unclassified_data_labels = np.zeros((num_test_data, 1));

# set vectors for descriptors and set string to write data to file
for i in range(len(descriptors)):
    descriptor = descriptors[i];
    unclassified_data[i, :] = descriptor.get_vector();
    unclassified_data_labels[i, :] = label_nums[descriptor.get_label()];

if normalize:
    # normalize data
    unclassified_data = unclassified_data /\
        unclassified_data.sum(axis=1)[:, np.newaxis];
    # remove NaNs
    unclassified_data[np.isnan(unclassified_data)] = 0;

training_data = np.zeros((num_training_data, vector_size + 1));

# go through all lines in training data file
for i in range(1, len(data_text_raw) - 1):
    items = data_text_raw[i].split('\t');
    label = label_nums[items[1]];
    vector_string = items[2];
    vector = [int(x) for x in vector_string.split()];
    vector.append(label);
    training_data[i, :] = vector;

training_data_predictors = training_data[:, :-1];
if normalize:
    training_data_predictors = training_data_predictors /\
        training_data_predictors.sum(axis=1)[:, np.newaxis];
    training_data_predictors[np.isnan(training_data_predictors)] = 0;
training_data_labels = training_data[:, -1];

clf = LogisticRegression(solver='newton-cg', C=1000000, max_iter=1000, random_state=0, \
    multi_class='multinomial', verbose=1).fit(training_data_predictors, \
    training_data_labels);

print('Logistic regression result:', clf.score(unclassified_data, unclassified_data_labels));

clf = KNeighborsClassifier(n_neighbors=50);
clf.fit(training_data_predictors, training_data_labels);

print('K nearest neighbors result:',clf.score(unclassified_data, unclassified_data_labels));

clf = MLPClassifier(solver='lbfgs', alpha=1e-5, \
        hidden_layer_sizes=(5, 2), random_state=1)

clf.fit(training_data_predictors, training_data_labels);

print('Multilayer perceptron result:',clf.score(unclassified_data, unclassified_data_labels));

clf = MultinomialNB();

clf.fit(training_data_predictors, training_data_labels);

print('Multinomial naive bayes result:',clf.score(unclassified_data, unclassified_data_labels));

clf = SVC(degree=1, kernel='poly', verbose=False);

clf.fit(training_data_predictors, training_data_labels);

print('Support vector machine result:',clf.score(unclassified_data, unclassified_data_labels));
