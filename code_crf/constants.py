# File: constants.py 
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen
# Created: 28/03/2018
#
# Description:
# Constants for use by multiple programs.

# folder containing text
TEXT_FOLDER = "data/text/";

# file containing sequences
SEQUENCES_FILE = "data/sequences";

# file containing labeled descriptors
DESCRIPTORS_LABELED_FILE = "data/descriptors_labeled";

# total number of episodes in the first generation
NUM_EPS = 116;

# format string for episode numbers
EP_NUMBER_FORMAT = '%03d';

# labels of descriptors
descriptor_labels = ['pokemon', 'person', 'settlement', 'move', 'event',\
    'item', 'region', 'building', 'group', 'type'];

# --- construct sequence labels ---

# add 'other' label to label words that are not parts of descriptors
sequence_labels = ['other']

# for each of the descriptor labels, create two sequence labels, one prefixed
# with 'b_' and the other prefixed with 'i_' to indicate that the label is for
# the first word of a descriptor or a subsequent word, respectively
sequence_labels += ['b_' + descriptor_label for \
    descriptor_label in descriptor_labels];
sequence_labels += ['i_' + descriptor_label for \
    descriptor_label in descriptor_labels];

START_LABEL = 'start';

# ---

# punctuation to consider as elements of the observation sequence, if they
# occur at the beginning or end of a word
punctation_observations = '",(){}[]:;'

# regex for matching descriptors; must be descriptor surrounded by
# non-alphabetical characters
descriptor_regex = r'[^A-Za-z]%s[^A-Za-z]';
