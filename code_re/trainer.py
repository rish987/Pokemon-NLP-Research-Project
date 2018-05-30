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

vectors_training = None;
labels_training = None;

vectors_test = None;
labels_test = None;

for filename in [TRAINING_TRIPLES_FILE, TEST_TRIPLES_FILE]:
    # parse in training triples file
    with open(filename, 'r') as file:
        lines = file.read().splitlines();

        # remove duplicates
        list(set(lines));

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

    if (filename == TRAINING_TRIPLES_FILE):
        labels_training = labels;
        vectors_training = vectors;
    else:
        labels_test = labels;
        vectors_test = vectors;

# TODO remove; filter out label entries from vector
#vectors = vectors[:, 10:-10];
# -

# number of data instances
data_num = vectors.shape[0];

# - split labels and vectors into training and test data -
num_training = vectors_training.shape[0];
num_test = vectors_test.shape[0];
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
    list_i = prediction_i;

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
