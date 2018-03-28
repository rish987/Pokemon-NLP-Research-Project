# File: parameter_estimator.py 
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen
# Created: 28/03/2018
#
# Description:
# Uses L-BFGS optimization to estimate parameters from training data, and
# writes parameters to file.
import math;
import functions;

# proportion of labeled sequence observations to use in training
TRAINING_PROP = 0.3;

"""
Generic binary function.

curr_state - the current state
prev_state - the previous state
observations - the observation sequence
time - the current time within the sequence
func_type - string representing the type of function to use
ex: first_letter_capitalized
"""
def function(curr_state, prev_state, observations, time, func_i):
    return functions.get_function(func_i)(curr_state, prev_state, \
        observations, time);

"""
Evaluates the factor for this set of (curr_state, prev_state, obs), using the
given function types and their corresponding parameters.

funcs_and_parameters - list of tuples associating indexed functions with their
parameters
curr_state - the current state
prev_state - the previous state
observations - the observation sequence
time - the current time within the sequence
"""
def factor(funcs_and_parameters, curr_state, prev_state, observations, time):
    # to store exponent sum
    exponent = 0;

    # go through all function types and their parameters
    for func_i, parameter in funcs_and_parameters:
        exponent += function(curr_state, prev_state, observations, \
            time, func_i) * parameter;

    # return e ^ exponent
    return math.exp(exponent);
