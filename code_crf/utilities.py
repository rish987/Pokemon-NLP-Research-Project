# File: utilities.py 
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen
# Created: 28/03/2018
# 
# Description:
# Outsourced utility functions, mostly to improve code readability.
from constants import *;

"""
Converts the given sentence to a mapping from text observations to their
original indices in the text.
"""
def sentence_to_indexed_observations(sentence):
    # is a word currently being parsed?
    in_word = False;

    # list of indices
    indices = [];

    # current character index
    index = 0;

    # go through all characters in the sentence
    for char in sentence:
        # found observation punctuation
        if char in punctation_observations:
            indices.append(index);
            in_word = False;
        # just left a word
        elif char == ' ' and in_word:
            in_word = False;
        # just entered a word
        elif char != ' ' and not in_word:
            in_word = True;
            indices.append(index);
        else:
            pass;

        index += 1;

    # get split words
    segments = sentence.split(' ');

    # total list of observation
    observations = [];

    # go through all space-delimited words in the sentence
    for segment in segments:
        # observations extracted from this segment
        segment_observations = [];

        # current observation
        observation = '';

        # go through all characters in this segment
        for char in segment:
            # this is punctuation observation
            if char in punctation_observations:
                # found an observation previously, must save
                if len(observation) > 0:
                    segment_observations.append(observation);
                # add this punctuation observation
                segment_observations.append(char);
                # reset observation
                observation = '';
            else:
                # add this character to the current observation
                observation += char;

        # found an observation previously, must save
        if len(observation) > 0:
            segment_observations.append(observation);

        observations += segment_observations;

    # create return mapping
    observations_to_indices = [];

    observation_index = 0;

    # observations and indices not parallel
    if len(indices) != len(observations):
        # print warning
        print("WARNING: Observations and indices not parallel.");

    # go through all observations
    for observation in observations:
        observations_to_indices.append((observation,\
            indices[observation_index]));
        observation_index += 1;

    return observations_to_indices;
