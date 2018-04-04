# File: functions.py 
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen
# Created: 28/03/2018
# 
# Description:
# Repository of functions for use by CRF model.
# TODO rename to feature_function
from constants import *;

"""
Returns 1 if the given word is capitalized, 0 otherwise;
"""
def is_capitalized(word):
    if word[0].isupper():
        return 1;
    return 0;

"""
Returns 1 if the given word is possessive, 0 otherwise;
"""
def is_possessive(word):
    if word.endswith('\'s'):
        return 1;
    return 0;

# --- constructing function list ---

# list of functions
functions = [];

# mapping of current states to relevant function indices
curr_state_to_func_inds = {};
for curr_label in sequence_labels:
    curr_state_to_func_inds[curr_label] = [];
# mapping of combinations of current states and previous states to relevant 
# function indices
curr_state_prev_state_to_func_inds = {};
for curr_label in sequence_labels:
    curr_state_prev_state_to_func_inds[curr_label] = {};
    for prev_label in (sequence_labels + [START_LABEL]):
        curr_state_prev_state_to_func_inds[curr_label][prev_label] = [];
# mappings of combinations of current states and previous/next observations to
# relevant function indices
curr_state_prev_obs_to_func_inds = {};
curr_state_prev2_obs_to_func_inds = {};
curr_state_next_obs_to_func_inds = {};
curr_state_curr_obs_to_func_inds = {};
for curr_label in sequence_labels:
    curr_state_prev_obs_to_func_inds[curr_label] = {};
    curr_state_prev2_obs_to_func_inds[curr_label] = {};
    curr_state_next_obs_to_func_inds[curr_label] = {};
    curr_state_curr_obs_to_func_inds[curr_label] = {};
    for pivot in pivots:
        for pivot_conj in pivots[pivot]:
            curr_state_prev2_obs_to_func_inds[curr_label][pivot_conj] = [];
            curr_state_prev_obs_to_func_inds[curr_label][pivot_conj] = [];
            curr_state_next_obs_to_func_inds[curr_label][pivot_conj] = [];
            curr_state_curr_obs_to_func_inds[curr_label][pivot_conj] = [];

# mapping of functions to their relevant states
functions_to_states = [];

# mapping of functions to their relevant previous states
functions_to_prev_states = [];

# create one of each function (set) for each sequence_label
for sequence_label in sequence_labels:
    # --- capitalized current word ---
    """
    1 if the current word is capitalized, 0 otherwise.
    """

    def curr_word_capitalized(curr_state, prev_state, observations, time, \
        sequence_label=sequence_label):
        if curr_state != sequence_label:
            return 0;
        return is_capitalized(observations[time]);
    functions.append(curr_word_capitalized);
    curr_state_to_func_inds[sequence_label].append(len(functions) - 1);
    functions_to_states.append([sequence_label]);
    functions_to_prev_states.append([ALL]);

    # --- 

    # --- capitalized previous word ---
    """
    1 if the there is a previous word and it is capitalized, 0 otherwise.
    """

    def prev_word_capitalized(curr_state, prev_state, observations, time, \
        sequence_label=sequence_label):
        if curr_state != sequence_label:
            return 0;
        if time - 1 < 0:
            return 0;
        return is_capitalized(observations[time - 1]);
    functions.append(prev_word_capitalized);
    curr_state_to_func_inds[sequence_label].append(len(functions) - 1);
    functions_to_states.append([sequence_label]);
    functions_to_prev_states.append([ALL]);

    # --- 

    # --- capitalized next word ---
    """
    1 if the there is a next word and it is capitalized, 0 otherwise.
    """

    def next_word_capitalized(curr_state, prev_state, observations, time, \
        sequence_label=sequence_label):
        if curr_state != sequence_label:
            return 0;
        if time + 1 >= len(observations):
            return 0;
        return is_capitalized(observations[time + 1]);
    functions.append(next_word_capitalized);
    curr_state_to_func_inds[sequence_label].append(len(functions) - 1);
    functions_to_states.append([sequence_label]);
    functions_to_prev_states.append([ALL]);

    # --- 

#    # --- possessive current word ---
#    """
#    1 if the current word is possessive, 0 otherwise.
#    """
#
#    def curr_word_possessive(curr_state, prev_state, observations, time, \
#        sequence_label=sequence_label):
#        if curr_state != sequence_label:
#            return 0;
#        return is_possessive(observations[time]);
#    functions.append(curr_word_possessive);
#    curr_state_to_func_inds[sequence_label].append(len(functions) - 1);
#    functions_to_states.append([sequence_label]);
#    functions_to_prev_states.append([ALL]);
#
#    # --- 
#
#    # --- possessive previous word ---
#    """
#    1 if the there is a previous word and it is possessive, 0 otherwise.
#    """
#
#    def prev_word_possessive(curr_state, prev_state, observations, time, \
#        sequence_label=sequence_label):
#        if curr_state != sequence_label:
#            return 0;
#        if time - 1 < 0:
#            return 0;
#        return is_possessive(observations[time - 1]);
#    functions.append(prev_word_possessive);
#    curr_state_to_func_inds[sequence_label].append(len(functions) - 1);
#    functions_to_states.append([sequence_label]);
#    functions_to_prev_states.append([ALL]);
#
#    # --- 
#
#    # --- possessive next word ---
#    """
#    1 if the there is a next word and it is possessive, 0 otherwise.
#    """
#
#    def next_word_possessive(curr_state, prev_state, observations, time, \
#        sequence_label=sequence_label):
#        if curr_state != sequence_label:
#            return 0;
#        if time + 1 >= len(observations):
#            return 0;
#        return is_possessive(observations[time + 1]);
#    functions.append(next_word_possessive);
#    curr_state_to_func_inds[sequence_label].append(len(functions) - 1);
#    functions_to_states.append([sequence_label]);
#    functions_to_prev_states.append([ALL]);
#
#    # --- 

    # --- previous label ---
    """
    Create one function for every possible (prev_state, curr_state) pair.
    Invalid transitions:
    other -> i_*
    b_a -> i_b
    i_a -> i_b
    """

    # label stripped of prefix
    curr_label_type = sequence_label[len(B_PREFIX):];
    for prev_sequence_label in (sequence_labels + [START_LABEL]):
        prev_label_type = prev_sequence_label[len(B_PREFIX):];

        if ((prev_sequence_label == OTHER) and sequence_label.startswith(\
                I_PREFIX)
            or (prev_sequence_label.startswith(B_PREFIX) \
                and sequence_label.startswith(I_PREFIX) and \
                prev_label_type != curr_label_type)
            or (prev_sequence_label.startswith(I_PREFIX) \
                and sequence_label.startswith(I_PREFIX) and \
                prev_label_type != curr_label_type)):
            continue;
        def prev_label(curr_state, prev_state, observations, time, \
            sequence_label=sequence_label,
            prev_sequence_label=prev_sequence_label):
            if curr_state == sequence_label and prev_state == \
            prev_sequence_label :
                return 1;
            return 0;

        functions.append(prev_label);
        curr_state_prev_state_to_func_inds[sequence_label]\
            [prev_sequence_label].append(len(functions) - 1);
        functions_to_states.append([sequence_label]);
        functions_to_prev_states.append([prev_sequence_label]);

    # --- 

    # --- previous observation pivot ---
    """
    Create one function for each of a list of predefined 'pivot' terms that is
    set if the previous observation is that pivot.
    """

    for pivot in pivots:
        pivot_conjs = pivots[pivot];
        def prev_word_pivot(curr_state, prev_state, observations, time, \
            sequence_label=sequence_label,
            pivot_conjs=pivot_conjs):
            if curr_state != sequence_label:
                return 0;
            if time - 1 < 0:
                return 0;
            if observations[time - 1].lower() in pivot_conjs:
                #print('here')
                return 1;
            else: 
                return 0;
        functions.append(prev_word_pivot);
        for pivot_conj in pivot_conjs:
            curr_state_prev_obs_to_func_inds[sequence_label][pivot_conj]\
                .append(len(functions) - 1);
        functions_to_states.append([sequence_label]);
        functions_to_prev_states.append([ALL]);

    # ---

    # --- 2nd previous observation pivot ---
    """
    Create one function for each of a list of predefined 'pivot' terms that is
    set if the 2nd previous observation (the observation before the previous
    observation) is that pivot.
    """

    for pivot in pivots:
        pivot_conjs = pivots[pivot];
        def prev2_word_pivot(curr_state, prev_state, observations, time, \
            sequence_label=sequence_label,
            pivot_conjs=pivot_conjs):
            if curr_state != sequence_label:
                return 0;
            if time - 2 < 0:
                return 0;
            if observations[time - 2].lower() in pivot_conjs:
                return 1;
            else: 
                return 0;
        functions.append(prev2_word_pivot);
        for pivot_conj in pivot_conjs:
            curr_state_prev2_obs_to_func_inds[sequence_label][pivot_conj]\
                .append(len(functions) - 1);
        functions_to_states.append([sequence_label]);
        functions_to_prev_states.append([ALL]);

    # ---

    # --- next observation pivot ---
    """
    Create one function for each of a list of predefined 'pivot' terms that is
    set if the next observation is that pivot.
    """

    for pivot in pivots:
        pivot_conjs = pivots[pivot];
        def next_word_pivot(curr_state, prev_state, observations, time, \
            sequence_label=sequence_label,
            pivot_conjs=pivot_conjs):
            if curr_state != sequence_label:
                return 0;
            if time + 1 >= len(observations):
                return 0;
            if observations[time + 1].lower() in pivot_conjs:
                #print('here')
                return 1;
            else: 
                return 0;
        functions.append(next_word_pivot);
        for pivot_conj in pivot_conjs:
            curr_state_next_obs_to_func_inds[sequence_label][pivot_conj]\
                .append(len(functions) - 1);
        functions_to_states.append([sequence_label]);
        functions_to_prev_states.append([ALL]);

    # ---

    # --- current observation pivot ---
    """
    Create one function for each of a list of predefined 'pivot' terms that is
    set if the current observation is that pivot.
    """

    for pivot in pivots:
        pivot_conjs = pivots[pivot];
        def current_word_pivot(curr_state, prev_state, observations, time, \
            sequence_label=sequence_label,
            pivot_conjs=pivot_conjs):
            if curr_state != sequence_label:
                return 0;
            if observations[time].lower() in pivot_conjs:
                #print('here')
                return 1;
            else: 
                return 0;
        functions.append(current_word_pivot);
        for pivot_conj in pivot_conjs:
            curr_state_curr_obs_to_func_inds[sequence_label][pivot_conj]\
                .append(len(functions) - 1);
        functions_to_states.append([sequence_label]);
        functions_to_prev_states.append([ALL]);

    # ---

# ---
