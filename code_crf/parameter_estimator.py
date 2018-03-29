# File: parameter_estimator.py 
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen
# Created: 28/03/2018
#
# Description:
# Uses L-BFGS optimization to estimate parameters from training data, and
# writes parameters to file.
import math;
import numpy as np;
import functions;
import pickle;
from constants import *;

# proportion of labeled sequence observations to use in training
TRAINING_PROP = 0.3;

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
    # to store exponent sum
    exponent = 0;

    # current funtion index
    func_i = 0;
    
    # go through all function types and their parameters
    for index in functions.labels_to_func_inds[curr_state]:
        exponent += functions.functions[index](curr_state, prev_state, \
        observations, time) * parameters[index];

        func_i += 1;

    # return e ^ exponent
    return math.exp(exponent);

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
                prev_states = ['start'];

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

sequences = None;
with open(SEQUENCES_FILE, 'rb') as file:
    sequences = pickle.load(file);

test_obss = sequences[0][0];
test_params = np.random.rand(len(functions.functions), 1) - 0.5;
forward_calc(test_params, test_obss);
print(forward_values);
