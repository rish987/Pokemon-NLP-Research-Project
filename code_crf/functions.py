# File: functions.py 
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen
# Created: 28/03/2018
# 
# Description:
# Repository of functions for use by CRF model.
# TODO further improve runtime by breaking down labels_to_func_inds into
# 'common' function indices and lists of function indices for particular 
# prev_states and 
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

# mapping of functions to their relevant states
functions_to_states = [];

# mapping of functions to their relevant previous states
functions_to_prev_states = [];

# create one of each function (set) for each sequence_label
for sequence_label in sequence_labels:
    labels_to_func_inds[sequence_label] = {};

    labels_to_func_inds[sequence_label][COMMON] = [];
    labels_to_func_inds[sequence_label][START_LABEL] = [];
    for prev_state in sequence_labels:
        labels_to_func_inds[sequence_label][prev_state] = [];

    # --- capitalized current word ---

    def curr_word_capitalized(curr_state, prev_state, observations, time, \
        sequence_label=sequence_label):
        if curr_state != sequence_label:
            return 0;
        return is_capitalized(observations[time]);
    functions.append(curr_word_capitalized);
    labels_to_func_inds[sequence_label][COMMON].append(len(functions) - 1);
    functions_to_states.append([sequence_label]);
    functions_to_prev_states.append([ALL]);

    # --- 

    # --- previous label ---

    for prev_sequence_label in (sequence_labels + [START_LABEL]):
        def prev_label(curr_state, prev_state, observations, time, \
            sequence_label=sequence_label,
            prev_sequence_label=prev_sequence_label):
            if curr_state == sequence_label and prev_state == \
            prev_sequence_label :
                return 1;
            return 0;

        functions.append(prev_label);
        labels_to_func_inds[sequence_label][prev_sequence_label].append(\
            len(functions) - 1);
        functions_to_states.append([sequence_label]);
        functions_to_prev_states.append([prev_sequence_label]);

    # --- 

# ---
