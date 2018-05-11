# File: constants.py 
# Author(s): Rishikesh Vaishnav, TODO
# Created: 17/04/2018

# file containing labeled descriptors
DESCRIPTORS_LABELED_FILE = "data/descriptors_labeled";

# file containing OpenIE output
OPENIE_OUTPUT_FILE = "data/openie_out";

# file containing sorted relation tuples with originating text
SORTED_TUPLES_FILE = "data/sorted_tuples";

# file containing output from training sentence finder
RELATION_SENTENCES_FILE = "data/relation_sentences" ;

# labels of descriptors
descriptor_labels = ['pokemon', 'person', 'settlement', 'move', 'event',\
    'item', 'region', 'building', 'group', 'type'];

# descriptor labels sorted alphabetically
descriptor_labels_alpha = sorted(descriptor_labels) ;

# total number of episodes in the first generation
NUM_EPS = 116;

# format string for episode numbers
EP_NUMBER_FORMAT = '%03d';

def get_dictionary_desc_to_labels ():
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

    return descriptors_to_labels, descriptors_ordered ;
