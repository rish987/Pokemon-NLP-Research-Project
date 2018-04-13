# File: parameter_estimator.py 
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen
# Created: 28/03/2018
#
# Description:
# Uses L-BFGS optimization to estimate parameters from training data, and
# writes parameters to file.
# TODO implement algorithms log-style as in 4.38 (page 330)?
import math;
import numpy as np;
import functions;
import pickle;
import threading;
from decimal import *;
from termcolor import colored;
from scipy.optimize import fmin_l_bfgs_b;
from constants import *;

# to store results of iterations in an ordered list of (accuracy, parameters)
# tuples
iteration_results = [];

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
    # get indices of functions that only require the current state
    func_indices = functions.curr_state_to_func_inds[curr_state];
    # get indices of functions that require the current state and the previous
    # state
    func_indices = func_indices \
        + functions.curr_state_prev_state_to_func_inds[curr_state][prev_state];
    if time - 1 >= 0:
        prev_obs = observations[time - 1].lower();
        if prev_obs in functions.curr_state_prev_obs_to_func_inds[curr_state]:
            # get indices of functions that require the current state, previous
            # state and previous observation
            func_indices = func_indices \
                + functions.curr_state_prev_obs_to_func_inds[curr_state]\
                [prev_obs];
    if (time - 2) >= 0:
        prev2_obs = observations[time - 2].lower();
        if prev2_obs in functions.curr_state_prev2_obs_to_func_inds[curr_state]:
            # get indices of functions that require the current state, previous
            # state and previous observation
            func_indices = func_indices \
                + functions.curr_state_prev2_obs_to_func_inds[curr_state]\
                [prev2_obs];
    if (time + 1) < len(observations):
        next_obs = observations[time + 1].lower();
        if next_obs in functions.curr_state_next_obs_to_func_inds[curr_state]:
            # get indices of functions that require the current state next
            # observation
            func_indices = func_indices \
                + functions.curr_state_next_obs_to_func_inds[curr_state]\
                [next_obs];
    curr_obs = observations[time].lower();
    if curr_obs in functions.curr_state_curr_obs_to_func_inds[curr_state]:
        # get indices of functions that require the current state and current
        # observation
        func_indices = func_indices \
            + functions.curr_state_curr_obs_to_func_inds[curr_state]\
            [curr_obs];
    # ---

    # go through all function types and their parameters
    for index in func_indices:
        #print('parameter: ' + str(parameters[index]));
        total += functions.functions[index](curr_state, prev_state, \
        observations, time) * parameters[index];

    return Decimal(total);

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
    # return 0 if this is an impossible transition
    curr_label_type = curr_state[len(B_PREFIX):];
    prev_label_type = prev_state[len(B_PREFIX):];
    if ((prev_state == OTHER) and curr_state.startswith(I_PREFIX)
        or (prev_state.startswith(B_PREFIX) and \
            curr_state.startswith(I_PREFIX) and \
            prev_label_type != curr_label_type) \
        or (prev_state.startswith(I_PREFIX) and \
            curr_state.startswith(I_PREFIX) and \
            prev_label_type != curr_label_type)):
        return 0;
    # return e ^ (weighted function sum)
    return weighted_function_sum(parameters, curr_state, prev_state, \
            observations, time).exp();

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

                if time > 0:
                    if forward_values[prev_state][time - 1] == 0:
                       continue;
                    else:
                        # get the factor of transitioning from this previous
                        # state
                        this_factor = factor(parameters, curr_state, \
                            prev_state, observations, time);
                        # adjust the forward value of this state at this time
                        forward_values[curr_state][time] += this_factor * \
                            forward_values[prev_state][time - 1];
                else:
                    this_factor = factor(parameters, curr_state, \
                        prev_state, observations, time);
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
                if backward_values[next_state][time + 1] == 0:
                    continue;
                else:
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

    if forward_value != 0:
        return ((forward_value \
               * factor(parameters, curr_state, prev_state, observations, time)\
               * backward_values[curr_state][time]) / this_z_val);
    else:
        return 0;

"""
Returns the negative likelihood function and its gradient, calculated for the
given observation and label training sequences and the given parameters.

parameters - model parameters to use in calculation
sequences - list of (observation_sequence, label_sequence) training pairs
reg_param - regularization parameter, 1/(2*sigma^2) from equation 5.4
TODO remove test_sequences
"""
def neg_likelihood_and_gradient(parameters, sequences, reg_param, \
    test_sequences):

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
        for time in range(len(observations)):
            for param_i in range(len(parameters)):
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
        print('this_z_val: ' + str(this_z_val));
        den_sum_l += this_z_val.ln();
        # --- 

        # --- adjust gradient denominator ---
        backward_calc(parameters, observations);
        # go over all times
        for time in range(len(observations)):
            # go through all parameter indices
            for param_i in range(len(parameters)):
                # only consider applicable states
                curr_states = functions.functions_to_states[param_i];
                # if this is not the first observation, consider all of the
                # states as possible previous states
                # TODO limit to possible states
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
                        if term != 0:
                            term *= state_pair_probability(parameters, \
                                    curr_state, prev_state, observations, \
                                    time, this_z_val);
                        den_sum_g[param_i] += term;
        # --- 

        sequence_i += 1;

    # ---
    # calculate squared sum of parameters
    sqr_param_sum = 0;
    for parameter in parameters:
        sqr_param_sum += parameter ** 2;

    likelihood = num_sum_l - den_sum_l - Decimal(reg_param * sqr_param_sum);
    gradient = np.array(num_sum_g, dtype=np.float64) - \
	np.array(den_sum_g, dtype=np.float64) - \
	(reg_param * 2 * np.array(parameters, dtype=np.float64));

    # negate and return likelihood and gradient
    neg_likelihood = -1 * likelihood;
    neg_gradient = -1 * gradient;

    ret = (neg_likelihood, neg_gradient);

    accuracy = evaluate(parameters, test_sequences, True);
    print(neg_likelihood);
    print(accuracy);
    iteration_results.append((accuracy, convert_param_list_to_mapping\
        (list(parameters.tolist()))));
    # write sequences to file
    with open(ITERATION_RESULTS_FILE, 'wb') as file:
        pickle.dump(iteration_results, file);

    return ret;

"""
Evaluates the specified model on the given list of observations sequences,
returning the percentage of labels correctly predicted.
"""
def evaluate(parameters, sequences, print_results):
    num_correct = 0;
    total = 0;
    for observations, labels in sequences:
        pred_labels = max_calc(parameters, observations);
        if print_results:
            print("\n" + "Observation".ljust(TEXT_WIDTH) + '|'\
                + "Match".ljust(7) + '|'\
                + "Predicted Label".ljust(TEXT_WIDTH) + '|'\
                + "Observed Label".ljust(TEXT_WIDTH));
            print('-' * ((TEXT_WIDTH * 3) + 2 + 8));
             
        for label_i in range(len(labels)):
            match = labels[label_i] == pred_labels[label_i];
            color = 'green' if match else 'red';
            match_str = colored('+', color) if match else colored('-', color);

            if print_results:
                print(observations[label_i].ljust(TEXT_WIDTH) + '|'\
                    + '   ' + match_str + '   |'\
                    + colored(pred_labels[label_i].ljust(TEXT_WIDTH), color)\
                    + '|' + colored(labels[label_i].ljust(TEXT_WIDTH), color));
            if (labels[label_i] != OTHER):
                if (labels[label_i] == pred_labels[label_i]):
                    num_correct += 1;
                total += 1;

    return float(num_correct) / float(total);

"""
Converts the given list of parameters to a mapping from function names to
parameters.
"""
def convert_param_list_to_mapping(params):
    mapping = {};
    for func_name in functions.func_names_to_func_inds:
        func_ind = functions.func_names_to_func_inds[func_name];
        mapping[func_name] = params[func_ind];

    return mapping;

# TODO testing... remove
sequences = None;
with open(SEQUENCES_FILE, 'rb') as file:
    sequences = pickle.load(file);

num_training = 100;
num_test = 100;
training_seqs = sequences[0:num_training]\
        + sequences[(num_training + num_test):(num_training + num_test\
        + num_training)] ;
test_seqs = sequences[num_training:(num_training + num_test)];
with open(ITERATION_RESULTS_FILE, 'rb') as file:
    iteration_results_loaded = pickle.load(file);

#iteration_results_to_write = [];
#for result in iteration_results_loaded:
#    iteration_results_to_write.append((result[0],
#        convert_param_list_to_mapping(result[1])));
#
#with open(ITERATION_RESULTS_FILE, 'wb') as file:
#    pickle.dump(iteration_results_to_write, file);

params = [0] * len(functions.functions);
chosen_iteration_result = iteration_results_loaded[\
    len(iteration_results_loaded) - 1];

for func_name in chosen_iteration_result[1]:
    value = chosen_iteration_result[1][func_name];
    params[functions.func_names_to_func_inds[func_name]] = value;

accuracy = evaluate(params, test_seqs, True);
print("Accuracy: " + str(accuracy));

#best_iteration_result = max(iteration_results_loaded, key=lambda x:x[0]);
#print(best_iteration_result[0]);
#params = np.array(best_iteration_result[1]);
#if params.shape[0] != len(functions.functions):
#    print("WARNING: loaded parameters incorrect size.");

#params = np.zeros((len(functions.functions), 1));
#params = np.array(iteration_results_loaded[len(iteration_results_loaded) - 1][1]);
#fmin_l_bfgs_b(neg_likelihood_and_gradient, x0=params, fprime=None, \
#    args=(training_seqs, \
#    #1 / (2 * 1),\
#    0,\
#    test_seqs), approx_grad=False, \
#    bounds=None, m=10, \
#    factr=10000000.0, pgtol=1e-05, epsilon=1e-08, iprint=-1, \
#    maxfun=15000, maxiter=15000, disp=None, callback=None);
