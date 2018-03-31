# File: parameter_estimator.py 
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen
# Created: 28/03/2018
#
# Description:
# Uses L-BFGS optimization to estimate parameters from training data, and
# writes parameters to file.
# TODO implement algorithms log-style as in 4.38 (page 330)?
# TODO add regularization
import math;
import numpy as np;
import functions;
import pickle;
from scipy.optimize import fmin_l_bfgs_b;
from constants import *;

# proportion of labeled sequence observations to use in training
TRAINING_PROP = 0.3;

"""
Evaluates the weighted sum of all functions using the given parameters and
arguments.

parameters - list of function parameters
curr_state - the current state
prev_state - the previous state
observations - the observation sequence
time - the current time within the sequence
"""
def weighted_function_sum(parameters, curr_state, prev_state, observations, \
    time):
    # to store sum
    total = 0;

    # --- get indices of functions applicable to this curr_state and
    # prev_state ---
    func_indices = functions.labels_to_func_inds[curr_state][COMMON];
    func_indices = func_indices \
        + functions.labels_to_func_inds[curr_state][prev_state];
    # ---

    # go through all function types and their parameters
    for index in func_indices:
        total += functions.functions[index](curr_state, prev_state, \
        observations, time) * parameters[index];

    return total;

"""
Evaluates the factor for this set of (curr_state, prev_state, obs), using the
given parameters.

parameters - list of function parameters
curr_state - the current state
prev_state - the previous state
observations - the observation sequence
time - the current time within the sequence
"""
def factor(parameters, curr_state, prev_state, observations, time):
    # return e ^ (weighted function sum)
    return math.exp(weighted_function_sum(parameters, curr_state, prev_state, \
        observations, time));

# global data structures for storing forward and backward values
forward_values = {};
backward_values = {};

# global data structures for storing viterbi values and backpointers
max_values = {};
max_backpointers = {};

"""
Resets the forward values data structure to reflect the given parameters and
observations.
"""
def forward_calc(parameters, observations):
    # total number of observations in the sequence
    num_observations = len(observations);

    # --- initialize forward values data structure ---
    for state in sequence_labels:
        forward_values[state] = [0] * num_observations;
    # ---

    # --- set forward values data structure ---
    for time in range(num_observations):
        for curr_state in sequence_labels:
            # if this is not the first observation, consider all of the states
            # as possible previous states
            prev_states = sequence_labels;
            # if this is the first observation, consider only the start state
            # as a possible previous state
            if time == 0:
                prev_states = [START_LABEL];

            # go through all possible previous states
            for prev_state in prev_states:
                # get the factor of transitioning from this previous state
                this_factor = factor(parameters, curr_state, prev_state, \
                    observations, time);

                if time > 0:
                    # adjust the forward value of this state at this time
                    forward_values[curr_state][time] += this_factor * \
                        forward_values[prev_state][time - 1];
                else:
                    # adjust the forward value of this state at this time
                    forward_values[curr_state][time] += this_factor;

    # ---

"""
Resets the backward values data structure to reflect the given parameters and
observations.
"""
def backward_calc(parameters, observations):
    # total number of observations in the sequence
    num_observations = len(observations);

    # --- initialize backward values data structure ---
    for state in sequence_labels:
        backward_values[state] = [0] * num_observations;
        backward_values[state][num_observations - 1] = 1;
    # ---

    # --- set backward values data structure ---
    for time in list(reversed(range(num_observations)))[1:]:
        for curr_state in sequence_labels:
            # go through all possible next states
            for next_state in sequence_labels:
                # get the factor of transitioning to this next state
                this_factor = factor(parameters, next_state, curr_state, \
                    observations, time + 1);

                # adjust the backward value of this state at this time
                backward_values[curr_state][time] += this_factor * \
                    backward_values[next_state][time + 1];

    # ---

"""
Uses the Viterbi algorithm to reset the max values and backpointers data
structure to reflect the given parameters and observations. Returns the maximum
likelihood sequence.
"""
def max_calc(parameters, observations):
    # total number of observations in the sequence
    num_observations = len(observations);

    # --- initialize max values data structures ---
    for state in sequence_labels:
        max_values[state] = [0] * num_observations;
        max_backpointers[state] = [None] * num_observations;
    # ---

    # --- set max values data structures ---
    for time in range(num_observations):
        for curr_state in sequence_labels:
            # if this is not the first observation, consider all of the states
            # as possible previous states
            prev_states = sequence_labels;
            # if this is the first observation, consider only the start state
            # as a possible previous state
            if time == 0:
                prev_states = [START_LABEL];

            # go through all possible previous states
            for prev_state in prev_states:
                # get the factor of transitioning from this previous state
                this_factor = factor(parameters, curr_state, prev_state, \
                    observations, time);

                # original max value
                original_max = max_values[curr_state][time]

                if time > 0:
                    # adjust the max value of this state at this time
                    max_values[curr_state][time] =\
                        max(original_max,\
                        this_factor * max_values[prev_state][time - 1]);
                else:
                    # adjust the max value of this state at this time
                    max_values[curr_state][time] =\
                        max(original_max,\
                        this_factor);

                # the max was just reset
                if original_max < max_values[curr_state][time]:
                    # reset the backpointer
                    max_backpointers[curr_state][time] = prev_state;

    # ---

    # --- get maximum probability label sequence ---

    # to store the maximum probability label sequence
    max_prob_seq = [None] * num_observations;
    
    # --- --- get maximum probability final label --- ---
    # maximum-so-far final label max value and label
    final_max_value = 0;
    final_max_label = None;

    # go through all possible labels of last observation
    for label in sequence_labels:
        # the max should be reset
        if max_values[label][num_observations - 1] > final_max_value:
            final_max_value = max_values[label][num_observations - 1];
            final_max_label = label;

    # the current label
    curr_label = final_max_label;
    
    # go through all times, from end to beginning
    for time in list(reversed(range(num_observations))):
        max_prob_seq[time] = curr_label;

        # follow backpointer
        curr_label = max_backpointers[curr_label][time];
    # --- ---

    # ---

    return max_prob_seq;

"""
Returns the Z-value, as calculated from the current forward table.
Uses equation at the end of the first paragraph on page 318.
NOTE: This function assumes that forward_values is up to date.
"""
def z_val():
    z_val = 0;
    for state in sequence_labels:
        z_val += forward_values[state][len(forward_values[state]) - 1];

    return z_val;

"""
Calculates the probability of the specified current and previous states at the
specified time, given the specified observation sequence.
"""
def state_pair_probability(parameters, curr_state, prev_state, observations, \
    time, this_z_val):

    forward_value = 0;
    # use 1 as a forward value if the previous state is a start state
    if prev_state == START_LABEL:
        forward_value = 1;
    else:
        forward_value = forward_values[prev_state][time - 1];

    return ((forward_value \
           * factor(parameters, curr_state, prev_state, observations, time) \
           * backward_values[curr_state][time]) / this_z_val);

"""
Returns the negative likelihood function and its gradient, calculated for the
given observation and label training sequences and the given parameters.

parameters - model parameters to use in calculation
sequences - list of (observation_sequence, label_sequence) training pairs
TODO remove test_sequences
"""
def neg_likelihood_and_gradient(parameters, sequences, test_sequences):
    # initialize running numerator and denominator sums
    num_sum_l = 0;
    den_sum_l = 0;
    num_sum_g = [0] * len(parameters);
    den_sum_g = [0] * len(parameters);


    # --- calculate numerator ---
    
    print("calculating numerator");
    sequence_i = 0;

    # sum over all training instances
    for observations, labels in sequences:
        print('on sequence: ' + str(sequence_i + 1) + '/' + \
            str(len(sequences)));

        # --- adjust likelihood numerator ---
        for time in range(len(observations)):
            if time == 0:
                num_sum_l += weighted_function_sum(parameters, labels[time],\
                    START_LABEL, observations, time);
            else:
                num_sum_l += weighted_function_sum(parameters, labels[time],\
                    labels[time - 1], observations, time);
        # --- 

        # --- adjust gradient numerator ---
        # go through all parameter indices
        # TODO combine with above loop?
        for param_i in range(len(parameters)):
            for time in range(len(observations)):
                # use START_LABEL as previous state
                if time == 0:
                    num_sum_g[param_i] += functions.functions[param_i]\
                        (labels[time], START_LABEL, observations, time)
                # use actual previous state
                else:
                    num_sum_g[param_i] += functions.functions[param_i]\
                        (labels[time], labels[time - 1], observations, time)
        # --- 

        sequence_i += 1;

    # ---

    # --- calculate denominator ---
    
    print("calculating denominator");
    sequence_i = 0;
    # sum over all training instances
    for observations, labels in sequences:
        print('on sequence: ' + str(sequence_i + 1) + '/' + \
            str(len(sequences)));

        # --- adjust likelihood denominator ---
        forward_calc(parameters, observations);
        this_z_val = z_val();
        den_sum_l += math.log(this_z_val);
        # --- 

        # --- adjust gradient denominator ---
        backward_calc(parameters, observations); # TODO
        # go through all parameter indices
        for param_i in range(len(parameters)):
            # go over all times
            for time in range(len(observations)):
                # only consider applicable states
                curr_states = functions.functions_to_states[param_i];
                # if this is not the first observation, consider all of the
                # states as possible previous states
                prev_states = functions.functions_to_prev_states[param_i];
                if prev_states[0] == ALL:
                    prev_states = sequence_labels;
                # if this is the first observation, consider only the start
                # state as a possible previous state
                if time == 0:
                    prev_states = [START_LABEL];
                # go through all possible pairs of states 
                for curr_state in curr_states:
                    for prev_state in prev_states:
                        term = functions.functions[param_i]\
                            (curr_state, prev_state, observations, time);
                        term *= state_pair_probability(parameters, curr_state, \
                                prev_state, observations, time, this_z_val);
                        den_sum_g[param_i] += term;
        # --- 

        sequence_i += 1;

    # ---

    # negate and return likelihood and gradient
    neg_likelihood = -1 * (num_sum_l - den_sum_l);
    neg_gradient = -1 * (np.array(num_sum_g , dtype=np.float64) - \
	np.array(den_sum_g , dtype=np.float64));

    ret = (neg_likelihood, neg_gradient);

    print(neg_likelihood);
    print(evaluate(parameters, test_sequences));

    return ret;

"""
Evaluates the specified model on the given list of observations sequences,
returning the percentage of labels correctly predicted.
"""
def evaluate(parameters, sequences):
    num_correct = 0;
    total = 0;
    for observations, labels in sequences:
        pred_labels = max_calc(parameters, observations);
        for label_i in range(len(labels)):
            if (labels[label_i] != OTHER):
                if (labels[label_i] == pred_labels[label_i]):
                    print(labels[label_i]);
                    num_correct += 1;
                total += 1;

    return float(num_correct) / float(total);

# TODO testing... remove
sequences = None;
with open(SEQUENCES_FILE, 'rb') as file:
    sequences = pickle.load(file);

num_training = 20;
num_test = 30;
params = np.zeros((len(functions.functions), 1));
fmin_l_bfgs_b(neg_likelihood_and_gradient, params, fprime=None, \
    args=(sequences[0:num_training - 1], \
    sequences[num_training:(num_training + num_test) - 1]), approx_grad=False, \
    bounds=None, m=10, \
    factr=10000000.0, pgtol=1e-05, epsilon=1e-08, iprint=-1, \
    maxfun=15000, maxiter=15000, disp=None, callback=None);
