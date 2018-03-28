# File: sequence_constructor.py 
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen
# Created: 28/03/2018
#
# Description:
# Parses episode text into sentence-delimited observation sequences and their
# corresponding label sequences, storing them in a list of
# (observation_sequence, label_sequence) tuples, and writing this list to the
# file SEQUENCES_FILE.
from constants import *;
import utilities;
import pickle;
import re;

# --- get a dictionary mapping descriptors to their labels, and a list of
# ordered descriptors ---
# to hold mapping of descriptors to labels
descriptors_to_labels = {};

# open file and save lines to array
descriptors_labeled_file_lines = [];
with open(DESCRIPTORS_LABELED_FILE, 'r') as file:
    descriptors_labeled_file_lines = file.read().splitlines();


# construct dictionary mapping
for line in descriptors_labeled_file_lines:
    split = line.split('\t');
    label = split[0];
    descriptor = split[1];
    descriptors_to_labels[descriptor] = label;

# to hold descriptors ordered by length
descriptors_ordered = list(descriptors_to_labels.keys());

descriptors_ordered = \
    list(reversed(sorted(descriptors_ordered, key=lambda x: len(x))));
# ---

# to store (observation_sequence, label_sequence) tuples
sequences = [];

# go through all episodes
for ep_num in range(1, NUM_EPS + 1):
    print('Processing episode: ' + str(ep_num) + '/' + \
        str(NUM_EPS));
    # get text for this episode
    text_filename = TEXT_FOLDER + (EP_NUMBER_FORMAT % ep_num);
    text = '';
    with open(text_filename, 'r') as text_file:
        text = text_file.read();

    # --- get sentences of text ---

    # TODO replace naive '.'-delimited segmentation with more accurate
    # algorithm, such as HMM
    sentences = text.split('.');
    # remove empty sentences
    sentences = [sentence for sentence in sentences if len(sentence) > 0];

    # ---

    sentence_index = 0;

    # go through all sentences
    for sentence in sentences:
        print('Processing sentence: ' + str(sentence_index + 1) + '/' + \
            str(len(sentences)));
        # pad on spaces to be able to identify descriptors at the very end and
        # beginning
        sentence = ' ' + sentence + ' ';
        # to store this sentence's parallel observation and label sequences
        sequence_tuple = None;
        observations = [];
        labels = [];
        
        # --- get observation sequence ---
        # get mapping of observation to indices
        observations_to_indices = utilities.sentence_to_indexed_observations(
                sentence);
        observations_to_indices = \
            sorted(observations_to_indices, key=lambda x: x[1])
        observations = [x[0] for x in observations_to_indices];
        # ---

        # --- TODO get label sequence ---
        # to hold mapping from ranges to labels; ranges tuple (index of first
        # character, index of last character)
        descriptor_ranges_to_labels = {};

        # go through all descriptors in order from large to small
        for descriptor in descriptors_ordered:
            r = re.compile(descriptor_regex % re.escape(descriptor));
            iterator = r.finditer(sentence);
            for match in iterator:
                # actual range of the match, considering regex used
                actual_range = (match.span()[0] + 1, match.span()[1] - 2);
                # is the range of this match overlapping with an existing
                # range?
                match_range_invalid = False;

                # go through all previously added ranges
                for this_range in descriptor_ranges_to_labels:
                    # this match's range overlaps with another, so ignore this
                    # descriptor
                    if (actual_range[0] >= this_range[0] and \
                        actual_range[0] <= this_range[1])\
                        or (actual_range[1] >= this_range[0] and \
                        actual_range[1] <= this_range[1]):
                        match_range_invalid = True;
                        break;

                # valid, unused range
                if not match_range_invalid:
                    descriptor_ranges_to_labels[actual_range] = \
                    descriptors_to_labels[descriptor];

        for observation, observation_index in observations_to_indices:
            # has a descriptor range that encapsulates this observation been
            # found?
            found_range = False;
            for this_range in descriptor_ranges_to_labels:
                this_label = descriptor_ranges_to_labels[this_range];
                # this observation is in this range, so add a beginning or
                # inner label to it
                if (observation_index >= this_range[0] and \
                        observation_index <= this_range[1]):
                    if observation_index == this_range[0]:
                        labels.append('b_' + this_label);
                    else:
                        labels.append('i_' + this_label);
                    found_range = True;
                    break;

            if not found_range:
                labels.append('other');

        # ---

        ## TODO remove
        #for i in range(len(observations)):
        #    print(observations[i] + '\t' + labels[i]);


        # construct the sequences tuple and add to list
        sequence_tuple = (observations, labels);
        sequences.append(sequence_tuple);

        sentence_index += 1;
    
# write sequences to file
with open(SEQUENCES_FILE, 'wb') as file:
    pickle.dump(sequences, file);
