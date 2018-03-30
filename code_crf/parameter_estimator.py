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

    # go through all function types and their parameters
    for index in functions.labels_to_func_inds[curr_state]:
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

# global data structure for storing forward values
forward_values = {};

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
        # print(time);
        for curr_state in sequence_labels:
            # print('curr_state: ' + curr_state);
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
Returns the negative likelihood function and its gradient, calculated for the
given observation and label training sequences and the given parameters.

parameters - model parameters to use in calculation
sequences - list of (observation_sequence, label_sequence) training pairs
"""
def neg_likelihood_and_gradient(parameters, sequences):
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
        z_val = z_val();
        den_sum_l += math.log(z_val);
        # --- 

        # --- adjust gradient denominator ---
        #backward_calc(parameters, observations); TODO
        # go through all parameter indices
        for param_i in len(parameters):
            # go over all times
            for time in range(len(observations)):
                # if this is not the first observation, consider all of the
                # states as possible previous states
                prev_states = sequence_labels;
                # if this is the first observation, consider only the start
                # state as a possible previous state
                if time == 0:
                    prev_states = [START_LABEL];
                # go through all possible pairs of states
                for curr_state in sequence_labels:
                    for prev_state in prev_states:
                        term = functions.functions[param_i]\
                            (curr_state, prev_state, observations, time);
                        # TODO define state_pair_probability
                        term *= state_pair_probability(curr_state, prev_state,\
                                observations, time, z_val);

        # --- 

        sequence_i += 1;

    # ---

    # negate and return likelihood and gradient
    neg_likelihood = -1 * (num_sum_l - den_sum_l);
    neg_gradient = -1 * (np.array(num_sum_g , dtype=np.float32) - \
	np.array(den_sum_g , dtype=np.float32));
    return (neg_likelihood, neg_gradient);

# TODO testing... remove
sequences = None;
with open(SEQUENCES_FILE, 'rb') as file:
    sequences = pickle.load(file);

test_seqs = sequences;
test_obss = sequences[0][0];
test_params = np.random.rand(len(functions.functions), 1) - 0.5;
likelihood, gradient = neg_likelihood_and_gradient(test_params, test_seqs[0:10]);
print(likelihood);
print(gradient);
