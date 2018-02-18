# File: classifier.py 
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen

# Created: 06/02/2018
import numpy as np;
from constants import *;
from sklearn.linear_model import LogisticRegression;
from sklearn.neighbors import KNeighborsClassifier;

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

descriptors = [];

# go through all lines in training data file
for i in range(1, len(data_text_raw)-1):
    items = data_text_raw[i].split('\t');
    descriptors.append(items[0]);
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

clf = LogisticRegression(solver='newton-cg', max_iter=1000, random_state=0, \
    multi_class='multinomial', verbose=1).fit(training_vectors, \
    training_labels);

predictions = clf.predict(test_vectors);

# TODO off by one when accessing descriptors?
for i in range(num_training + 1, num_data - 1):
    prediction = predictions[i - (num_training + 1)];
    if prediction != labels[i]:
        print("***Incorrect Prediction: " + descriptors[i - 1]);
        print("\t Actual - " + [k for k,v in label_nums.items() if v \
                == labels[i]][0]);
        print("\t Predicted - " + [k for k,v in label_nums.items() if v \
                == prediction][0]);
    else:
        print("---Correct Prediction: " + descriptors[i - 1]);
        print("\t Actual - " + [k for k,v in label_nums.items() if v \
                == labels[i]][0]);
        print("\t Predicted - " + [k for k,v in label_nums.items() if v \
                == prediction][0]);

print(descriptors[num_training + 1]);

print('Logistic regression result:', clf.score(test_vectors, test_labels));

clf = KNeighborsClassifier(n_neighbors=50);
clf.fit(training_vectors, training_labels);

print('K nearest neighbors result:',clf.score(test_vectors, test_labels));
