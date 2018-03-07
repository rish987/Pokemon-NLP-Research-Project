# File: vector_loader.py 
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen
# Created: 06/03/2018
import json;
from constants import *;
import sys;
sys.path.insert(0, 'objects')
from Instance import *;

VERB_PIVOTS_FILE = 'verb_pivots';

def create_shallow_pivot_dict(pivots):
    pivot_dict = {};
    for pivot in pivots:
        pivot_dict[pivot] = [pivot];

    return pivot_dict;

# create pivots list
pivots_list = [];
verb_pivots = json.load(open(VERB_PIVOTS_FILE));
pivots_list.append(verb_pivots);
SUBJECT_PRONOUNS = ['he', 'she', 'it', 'they'];
subject_pronouns_pivots = create_shallow_pivot_dict(SUBJECT_PRONOUNS);
pivots_list.append(subject_pronouns_pivots);
OBJECT_PRONOUNS = ['him', 'her', 'it', 'them'];
object_pronouns_pivots = create_shallow_pivot_dict(OBJECT_PRONOUNS);
pivots_list.append(object_pronouns_pivots);
POSSESSIVE_ADJECTIVES = ['his', 'her', 'its', 'their'];
possessive_adjectives_pivots = create_shallow_pivot_dict(POSSESSIVE_ADJECTIVES);
pivots_list.append(possessive_adjectives_pivots);
POSSESSIVE_PRONOUNS = ['his', 'hers', 'its', 'theirs'];
possessive_pronouns_pivots = create_shallow_pivot_dict(POSSESSIVE_PRONOUNS);
pivots_list.append(possessive_pronouns_pivots);
REFLEXIVE_PRONOUNS = ['himself', 'herself', 'itself', 'themselves'];
reflexive_pronouns_pivots = create_shallow_pivot_dict(REFLEXIVE_PRONOUNS);
pivots_list.append(reflexive_pronouns_pivots);
ETC = ['a', 'as', 'at', 'about', 'after', 'before', 'behind', 'below',\
        'but', 'by', 'for', 'from', 'in', 'into', 'like', 'of', 'off', 'on',\
        's', 'onto', 'over', 'since', 'than', 'through', 'to', 'under',\
        'until', 'up', 'upon', 'the',  'with', 'without'];
etc_pivots = create_shallow_pivot_dict(ETC);
pivots_list.append(etc_pivots);

# go through all episodes
for ep_num in range(1, NUM_EPS + 1):
    print('Processing episode: ' + str(ep_num) + '/' + \
        str(NUM_EPS));

    # get instance text for this episode
    instance_text_filename = INSTANCES_FOLDER + (EP_NUMBER_FORMAT % ep_num);
    instance_texts = [];
    with open(instance_text_filename, 'r') as instance_text_file:
        instance_texts = instance_text_file.readlines();

    # clear vector file for this episode
    vector_filename = VECTORS_FOLDER + (EP_NUMBER_FORMAT % ep_num);
    with open(vector_filename, 'w') as vector_file:
        vector_file.close();

    instance_i = 0;
    # go through all instance text lines
    for instance_text in instance_texts:
        print('\tProcessing instance: ' + str(instance_i + 1) + '/' + \
            str(len(instance_texts)));
        # write vector for this instance to file
        instance = Instance(instance_text, label_to_nums, pivots_list);
        instance.write_vector_to_file(vector_filename);
        instance_i += 1;
