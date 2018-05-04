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

# total number of episodes in the first generation
NUM_EPS = 116;

# format string for episode numbers
EP_NUMBER_FORMAT = '%03d';
