# File: classifier.py 
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen

# Created: 06/02/2018
import numpy as np;
from constants import *;
from sklearn.linear_model import LogisticRegression;
from sklearn.neighbors import KNeighborsClassifier;
from sklearn.dummy import DummyClassifier;
import random;

# load the raw data
filedata = None;
with open(RAW_TEXT_FILE, 'r') as file :
  filedata = file.read();

# open data file
with open(TRAINING_DATA_SELF_FILE, 'r') as f:
    data_text_raw = f.read().splitlines();

# get length of vector
vector_size = int(data_text_raw[0]);

del data_text_raw[0];

random.shuffle(data_text_raw);

num_data = len(data_text_raw);

data = np.zeros((num_data, vector_size + 1));

descriptors = [];
descriptors_to_labels = {};

# go through all lines in training data file
for i in range(0, len(data_text_raw)):
    items = data_text_raw[i].split('\t');

    descriptor = items[0];
    descriptors.append(descriptor);
    label = label_nums[items[1]];
    
    descriptors_to_labels[descriptor] = label;

    vector_string = items[2];
    vector = [float(x) for x in vector_string.split()];
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
confidences = clf.decision_function(test_vectors);

for i in range(num_training + 1, num_data):
    prediction = predictions[i - (num_training + 1)];
    confidence = confidences[i - (num_training + 1)][int(prediction)];
    actual_str = [k for k,v in label_nums.items() if v == labels[i]][0];
    prediction_str = [k for k,v in label_nums.items() if v == prediction][0];
    if prediction != labels[i]:
        print("***Incorrect Prediction (" + str(confidence) + "):" + descriptors[i]);
        print("\t Actual - " + actual_str);
        print("\t Predicted - " + prediction_str);
    else:
        print("---Correct Prediction: (" + str(confidence) + "):" + descriptors[i]);
        print("\t Actual - " + actual_str);
        print("\t Predicted - " + prediction_str);

descriptor_classifications = {};
# go through all test data
for i in range(len(test_labels)):
    # get corresponding descriptor for this point
    descriptor = descriptors[i + (num_training + 1)]

    # there is not an entry in the dictionary yet for this descriptor
    if descriptor not in descriptor_classifications:
        descriptor_classifications[descriptor] = [];

    # add this prediction to the list of predictions for this descriptor, along
    # with the confidence
    descriptor_classifications[descriptor].append((predictions[i],\
        float(confidences[i][int(predictions[i])])));

num_correct = 0;
for descriptor in descriptor_classifications:
    classifications = descriptor_classifications[descriptor];

    # to store the sum of the confidences for each label
    confidences_per_label = {};
    for label in label_nums:
        num = label_nums[label];
        confidences_per_label[num] = 0;

    for classification in classifications:
        confidences_per_label[classification[0]] += classification[1];

    # take a confidence vote
    descriptor_label_prediction = max(confidences_per_label,\
        key=confidences_per_label.get);
    confidence = max(confidences_per_label.values());
    actual_str = [k for k,v in label_nums.items() if v == \
        descriptors_to_labels[descriptor]][0];
    prediction_str = [k for k,v in label_nums.items() if v == \
        descriptor_label_prediction][0];
    if (descriptor_label_prediction != descriptors_to_labels[descriptor]):
        pass;
        print("*Incorrect Prediction (" + str(confidence) + "):" + \
            descriptor);
        print("\t Actual - " + actual_str);
        print("\t Predicted - " + prediction_str);
    else:
        print("-Correct Prediction (" + str(confidence) + "):" + \
            descriptor);
        print("\t Actual - " + actual_str);
        print("\t Predicted - " + prediction_str);
        num_correct += 1;

print('Logistic regression result:', clf.score(test_vectors, test_labels));

#clf = KNeighborsClassifier(n_neighbors=50);
#clf.fit(training_vectors, training_labels);
#
#print('K nearest neighbors result:',clf.score(test_vectors, test_labels));

print("Descriptor classification results: " + \
    str(float(num_correct) / float(len(descriptor_classifications))) );

clf = DummyClassifier(strategy='stratified');
clf.fit(training_vectors, training_labels);

print('Random result:',clf.score(test_vectors, test_labels));
