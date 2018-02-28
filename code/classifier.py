# File: classifier.py 
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen
# Created: 06/02/2018

import numpy as np;
from sklearn.linear_model import LogisticRegression;
from sklearn.linear_model import RidgeClassifier;
from sklearn.dummy import DummyClassifier;
import random;

from constants import *;

"""
Read the training data from file, and return the data in matrix form, along
with a list of corresponding descriptors and the a dictionary containing the 
labels of each of those descriptors.
"""
def get_data_info():
    # open data file
    with open(TRAINING_DATA_SELF_FILE, 'r') as f:
        data_text_raw = f.read().splitlines();

    # get length of vector
    vector_length = int(data_text_raw[0]);

    # remove vector length from data lines
    del data_text_raw[0];

    data_lines = data_text_raw;

    # total number of instances in the file
    num_data = len(data_lines);

    # set up vector with expected size
    data = np.zeros((num_data, vector_length + 2));

    # to hold descriptors of each data point
    descriptors = [];

    # to hold mapping from descriptors to their actual labels
    descriptors_to_labels = {};

    # go through all lines in training data file
    for i in range(0, len(data_lines)):
        # get list of info for this data point
        items = data_lines[i].split('\t');

        # retrieve descriptor and label number
        descriptor = items[0];
        descriptors.append(descriptor);
        label = label_nums[items[1]];
        
        # set the known label of this descriptor, if haven't already done so
        if descriptor not in descriptors_to_labels:
            descriptors_to_labels[descriptor] = label;

        # extract vector, including its label number and original index
        vector_string = items[2];
        vector = [float(x) for x in vector_string.split()];
        vector.append(label);
        vector.append(i);

        # add this vector to the data
        data[i, :] = vector;
    
    # return relevant data
    ret_dict = { \
    "data": data, \
    "descriptors": descriptors, \
    "descriptors_to_labels": descriptors_to_labels \
    }
    return ret_dict;

"""
Classify the given data by both instance and descriptor, and return the results.
"""
def classify(data, descriptors, descriptors_to_labels, print_predictions, \
    print_results):
    # number of data points
    num_data = data.shape[0];

    # randomly shuffle the data vectors
    np.random.shuffle(data);

    # extract the vectors, labels, and indices
    vectors = data[:, :-2];
    labels = data[:, -2];
    indices = data[:, -1];

    # number of vectors to use as training data
    num_training = int(TRAINING_SET_PROP * num_data);
    num_test = num_data - num_training;

    # extract first 'num_training' training vectors and labels
    training_vectors = vectors[:num_training, :];
    training_labels = labels[:num_training];
    training_indices = indices[:num_training];

    # extract remaining test vectors and labels
    test_vectors = vectors[num_training:, :];
    test_labels = labels[num_training:];
    test_indices = indices[num_training:];

    # set up logistic regression classifier and fit to data
    log_reg_clf = LogisticRegression(solver='newton-cg', max_iter=50, random_state=0,\
        multi_class='multinomial', verbose=0).fit(training_vectors, \
        training_labels);

    # get classifier's predictions and decision function for each vector
    predictions = log_reg_clf.predict(test_vectors);
    confidences = log_reg_clf.decision_function(test_vectors);

    # to record number of correctly classified instances
    num_correct_inst = 0;

    # to hold mapping from descriptor to list of predictions for that
    # descriptor
    descriptor_classifications = {};

    # go through all test data indices
    for i in range(num_test):

        # actual label number and string
        actual = test_labels[i];
        actual_str = [k for k,v in label_nums.items() if v == actual][0];

        # predicted label number and string
        prediction = predictions[i];
        prediction_str = [k for k,v in label_nums.items() if \
            v == prediction][0];

        # prediction confidence for prediction
        confidence = confidences[i][int(prediction)];

        if prediction != actual:
            if print_predictions:
                print("***Incorrect Prediction (" + str(confidence) + "):" + descriptors[i]);
                print("\t Actual - " + actual_str);
                print("\t Predicted - " + prediction_str);
        else:
            if print_predictions:
                print("---Correct Prediction: (" + str(confidence) + "):" + descriptors[i]);
                print("\t Actual - " + actual_str);
                print("\t Predicted - " + prediction_str);

            num_correct_inst += 1;

        # get corresponding descriptor for this point
        descriptor = descriptors[int(test_indices[i])];

        # there is not an entry in the dictionary yet for this descriptor
        if descriptor not in descriptor_classifications:
            descriptor_classifications[descriptor] = [];

        # add this prediction to the list of predictions for this descriptor,
        # along with the confidence
        descriptor_classifications[descriptor].append((predictions[i],\
            float(confidences[i][int(predictions[i])])));

    # to record number of correctly classified descriptors
    num_correct_desc = 0;

    # go through all descriptors
    for descriptor in descriptor_classifications:
        # extract list of (classification,confidence) pairs for this descriptor
        classifications = descriptor_classifications[descriptor];

        # to store the sum of the confidences for each label
        confidences_per_label = {};

        # go through all labels
        for label in label_nums:
            # initialize the confidence for this label as 0
            num = label_nums[label];
            confidences_per_label[num] = 0;

        # set confidences by summing confidences of classifications
        for classification in classifications:
            confidences_per_label[classification[0]] += classification[1];

        # take a confidence vote
        descriptor_label_prediction = max(confidences_per_label,\
            key=confidences_per_label.get);
        confidence = max(confidences_per_label.values());

        # extract actual and predicted descriptor labels
        actual_str = [k for k,v in label_nums.items() if v == \
            descriptors_to_labels[descriptor]][0];
        prediction_str = [k for k,v in label_nums.items() if v == \
            descriptor_label_prediction][0];

        if (descriptor_label_prediction != descriptors_to_labels[descriptor]):
            if print_predictions:
                print("*Incorrect Prediction (" + str(confidence) + "):" + \
                    descriptor);
                print("\t Actual - " + actual_str);
                print("\t Predicted - " + prediction_str);
        else:
            if print_predictions:
                print("-Correct Prediction (" + str(confidence) + "):" + \
                    descriptor);
                print("\t Actual - " + actual_str);
                print("\t Predicted - " + prediction_str);
            num_correct_desc += 1;

    log_reg_result = float(num_correct_inst) / float(num_data - num_training);

    desc_classify_result = float(num_correct_desc) / \
            float(len(descriptor_classifications));

    dummy_clf = DummyClassifier(strategy='stratified');
    dummy_clf.fit(training_vectors, training_labels);
    dummy_result = dummy_clf.score(test_vectors, test_labels)

    ridge_clf = RidgeClassifier(solver='auto');
    ridge_clf.fit(training_vectors, training_labels);
    ridge_result = ridge_clf.score(test_vectors, test_labels)

    if print_results:
        print('Ridge result: ' + str(ridge_result));
        print("Logistic Regression result: " + str(log_reg_result));
        print("Descriptor classification result: " + str(desc_classify_result));
        print('Random result: ' + str(dummy_result));

    # return relevant scores
    ret_dict = { \
    "ridge": ridge_result, \
    "log_reg": log_reg_result, \
    "desc_classify": desc_classify_result, \
    "dummy": dummy_result \
    }
    return ret_dict;
