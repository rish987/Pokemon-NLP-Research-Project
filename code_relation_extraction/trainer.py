# File: trainer.py 
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen
# Created: 11/05/2018
from constants import *;
from generate_vector import *;
from sklearn.linear_model import LogisticRegression;
from sklearn.dummy import DummyClassifier;
from random import shuffle;
from termcolor import colored;

# proportion of labeled data to use for training
TRAINING_PROP = 0.7;

# - read in training data -
# parallel lists to contain triple strings and their labels
triple_labels = [];
triple_strings = [];

# parse in training triples file
with open(TRAINING_TRIPLES_FILE, 'r') as file:
    lines = file.read().splitlines();

    shuffle(lines);

    # use first character of line as label
    triple_labels = [line[0] for line in lines];
    
    # use string after first two characters of line as triple string
    triple_strings = [line[2:] for line in lines];
# -

# - convert training data to numpy arrays -
labels = np.array([int(label) for label in triple_labels]);
vectors = np.array([generate_triple_vector(triple) for triple in\
    triple_strings]);
# -

# number of data instances
data_num = vectors.shape[0];

# - split labels and vectors into training and test data -
num_training = int(data_num * TRAINING_PROP);
num_test = data_num - num_training;

vectors_training = vectors[:num_training, :];
labels_training = labels[:num_training];

vectors_test = vectors[num_training:, :];
labels_test = labels[num_training:];
# -

# set up logistic regression classifier and fit to data
log_reg_clf = LogisticRegression(solver='newton-cg', max_iter=50,\
        random_state=0, multi_class='multinomial',
        verbose=0).fit(vectors_training, labels_training);

# get classifier's predictions and decision function for each vector
predictions = log_reg_clf.predict(vectors_test);

# go through all predictions
for prediction_i in range(predictions.shape[0]):
    prediction = predictions[prediction_i];
    actual = labels_test[prediction_i];

    match = (prediction == actual);

    color = 'green' if match else 'red';
    message_condition = 'CORRECT' if match else 'INCORRECT';

    # get list index in list of triple strings
    list_i = num_training + prediction_i;

    # get this triple
    triple = triple_strings[list_i].replace('\t', '|');
    
    print(colored('[' + message_condition +  ' ' + str(prediction) + '-' \
        + str(actual) + ']\t', color) + triple);

# report score
score = log_reg_clf.score(vectors_test, labels_test);
print("Model Score: " + str(score));

dummy_clf = DummyClassifier(strategy='stratified');
dummy_clf.fit(vectors_training, labels_training);
dummy_result = dummy_clf.score(vectors_test, labels_test);
print("Dummy Score: " + str(dummy_result));
