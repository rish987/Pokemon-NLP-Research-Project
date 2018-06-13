# File: constants.py 
# Author(s): Rishikesh Vaishnav, TODO
# Created: 17/04/2018

# RELATION-LABEL NUMBER CORRESPONDENCES
# 0 - None
# 1 - Person Owns Pokémon
# 2 - Pokémon Has Move
# 3 - Person In Settlement
# 4 - Person Calls for Move
import re;

# file containing labeled descriptors
DESCRIPTORS_LABELED_FILE = "data/descriptors_labeled";
TRIPLES_TO_DESC_TUPS_FILE = "data/triples_to_desc_tups";

# file containing OpenIE output
ALL_TEXT_FILE = "../data/data";

# file containing OpenIE output
OPENIE_OUTPUT_FILE = "data/openie_out";

# file containing sorted relation tuples with originating text
SORTED_TUPLES_FILE = "data/sorted_tuples";

# file containing output from training sentence finder
RELATION_SENTENCES_FILE = "data/relation_sentences" ;

# file containing output from training triple finder
RELATION_TRIPLES_FILE = "data/relation_triples" ;

# file containing labeled relation tuples
TRAINING_TRIPLES_FILE = "data/training_tuples";
TEST_TRIPLES_FILE = "data/test_tuples"

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

# location of raw triples
OPENIE_TRIPLES_FILE = "./data/openie_out" ;

def get_raw_triples():
    # get triple file and split into lines
    triple_filename = OPENIE_TRIPLES_FILE ;
    triple_strs = '';
    with open(triple_filename, 'r') as file:
        triple_strs = file.read().splitlines() ;

    triple_strs_split = [x.split('\t') for x in triple_strs];
    triple_strs_sep = [(x[1], x[2], x[3]) for x in triple_strs_split];

    return triple_strs_sep;

# --- get a dictionary mapping descriptors to their labels, and a list of
# ordered descriptors ---
# to hold mapping of descriptors to labels
descriptors_to_labels = {};

# open descriptor-to-label file and save lines to array
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

SUBJECT = 1
OBJECT = 3
DISTANCE_WEIGHT = 0
LENGTH_WEIGHT = 1

# finds the descriptor (if one exists) in the phrase and returns it
def get_desc (desc_phrase):
    # iterate through ordered descriptors
    for descriptor in descriptors_ordered:
        r = re.search(r'\b%s\b' % re.escape(descriptor), desc_phrase);

        if r != None:
            return descriptor;

    # no descriptor was found in the phrase
    return None ;

