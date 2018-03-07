# File: constants.py 
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen
# Created: 06/03/2018

# folder to write output to
TEXT_FOLDER = "data/text/";

# folder to write instances to
INSTANCES_FOLDER = "data/instances/";

# folder to write vectors to
VECTORS_FOLDER = "data/vectors/";

# total number of episodes in the first generation
NUM_EPS = 116;

# format string for episode numbers
EP_NUMBER_FORMAT = '%03d';

# numerical assignments of labels
label_to_nums = { 'pokemon': 0, 'person': 1, 'settlement': 2, 'move': 3,\
        'event':4, 'item': 5, 'region': 6, 'building':7,\
        'group':8, 'type': 9};
