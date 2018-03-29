# File: functions.py 
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen
# Created: 28/03/2018
# 
# Description:
# Repository of functions for use by CRF model.
from constants import *;

"""
Returns 1 if the given word is capitalized, 0 otherwise;
"""
def is_capitalized(word):
    if word[0].isupper():
        return 1;
    return 0;

# --- constructing function list ---

# list of functions
functions = [];

# mapping of labels to function indices
labels_to_func_inds = {};

# create one of each function (set) for each sequence_label
for sequence_label in sequence_labels:
    labels_to_func_inds[sequence_label] = [];

    # --- capitalized current word ---

    def curr_word_capitalized(curr_state, prev_state, observations, time, \
        sequence_label=sequence_label):
        if curr_state != sequence_label:
            return 0;
        return is_capitalized(observations[time]);
    functions.append(curr_word_capitalized);
    labels_to_func_inds[sequence_label].append(len(functions) - 1);

    # --- 

    # --- previous label ---

    for prev_sequence_label in (sequence_labels + ['start']):
        def prev_label(curr_state, prev_state, observations, time, \
            sequence_label=sequence_label,
            prev_sequence_label=prev_sequence_label):
            if curr_state == sequence_label and prev_state == \
            prev_sequence_label :
                return 1;
            return 0;

        functions.append(prev_label);
        labels_to_func_inds[sequence_label].append(len(functions) - 1);

    # --- 

# ---
