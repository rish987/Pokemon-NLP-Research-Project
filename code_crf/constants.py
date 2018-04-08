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

# file containing results of training iterations
ITERATION_RESULTS_FILE = "data/iteration_results/last_run";

# file containing labeled descriptors
DESCRIPTORS_LABELED_FILE = "data/descriptors_labeled";

# file containing pickle object mapping from descriptors to global pivots and
# their values
DESCRIPTORS_TO_GLOBAL_PIVOTS_FILE = "data/descriptors_to_global_pivots";

# total number of episodes in the first generation
NUM_EPS = 116;

# format string for episode numbers
EP_NUMBER_FORMAT = '%03d';

# labels of descriptors
descriptor_labels = ['pokemon', 'person', 'settlement', 'move', 'event',\
    'item', 'region', 'building', 'group', 'type'];

# --- construct sequence labels ---

# add 'other' label to label words that are not parts of descriptors
OTHER = 'other';
sequence_labels = [OTHER]

# beginning and inner descriptor label prefixes
B_PREFIX = 'b_';
I_PREFIX = 'i_';

# for each of the descriptor labels, create two sequence labels, one prefixed
# with 'b_' and the other prefixed with 'i_' to indicate that the label is for
# the first word of a descriptor or a subsequent word, respectively
sequence_labels += [B_PREFIX + descriptor_label for \
    descriptor_label in descriptor_labels];
sequence_labels += [I_PREFIX + descriptor_label for \
    descriptor_label in descriptor_labels];

START_LABEL = 'start';

# indicator that all sequence labels should be used
ALL = 'all';

# ---

# punctuation to consider as elements of the observation sequence, if they
# occur at the beginning or end of a word
punctation_observations = '",(){}[]:;'

# regex for matching descriptors; must be descriptor surrounded by
# non-alphabetical characters
descriptor_regex = r'[^A-Za-z]%s[^A-Za-z]';

# key of common function subsection in labels_to_func_inds
COMMON = 'common';

def create_shallow_pivot_dict(pivots):
    pivot_dict = {};
    for pivot in pivots:
        pivot_dict[pivot] = [pivot];

    return pivot_dict;

# pivot terms
PIVOTS = ['a', 'an', 'as', 'at', 'about', \
        'by', 'for', 'from', 'in', 'into', 'like', 'of', 'on',\
        'through', 'to', 'the', 'his', 'her', 'its', 'out'];
#PIVOTS = [];
pivots = create_shallow_pivot_dict(PIVOTS);

pivots["call"] = ["call", "called", "calls", "calling"];
pivots["become"] = ["become", "becoming", "became", "becomes"];
pivots["recall"] = ["recalling", "recall", "recalled", "recalls"];
pivots["tell"] = ["tells", "telling", "tell", "told"];
pivots["send"] = ["sends", "sending", "sent", "send"];
pivots["use"] = ["using", "used", "uses", "use"]
pivots["settlement"] = ["city", "town", "village"]
pivots["building"] = ["building", "hall", "laboratory", "institute", "gym", \
    "center", "centre", "nursery", "lighthouse", "tower",\
    "tech", "lab"];
pivots["region"] = ["island", "islands", "region", "route", "forest",\
    "plateau", "cave", "hq", "archipelago", "mountain", "street",\
    "camp", "zone", "park", "porta"];
pivots["item"] = ["ball", "badge", "potion", "balloon", "berry", "berries",\
    "submarine", "trophy", "stone", "egg"];
pivots["event"] = ["contest", "festival", "prix", "conference", "day"];
pivots["person"] = ["professor", "nurse", "trainer", "leader",\
    "breeder", "officer", "captain", "ranger", "boss", "man", "woman"];
pivots["group"] = ["squad", "team", "league"];
pivots["move"] = ["kick", "spin", "attack", "attacks",\
    "sting", "screen", "punch", "toss", "beam", "wave", "powder",\
    "dance", "shot", "chop", "ray", "missile", "bash", "drill",\
    "gas", "pump", "grip", "fang", "scratch", "claw"];

# TODO add: Dr., Lt., Mt., Mr., Mrs., Peak, St., 
# TODO plurals of label pivots
# TODO adjective pivots

# --- global pivots ---
global_pivots = {};
global_pivots['person'] = ["saying", "say", "said", "says"];
# --- 

# table text width
TEXT_WIDTH = 15;
