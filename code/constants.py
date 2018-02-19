# File: constants.py 
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen

# Created: 05/02/2018
import re;
import json;
import copy;

# numerical assignments of labels
label_nums = { 'pokemon': 0, 'person': 1, 'settlement': 2, 'move': 3,\
        'event':4, 'item': 5, 'region': 6, 'building':7,\
        'group':8, 'type': 9};

d = json.load(open('dictionary.json'))

# bulbapedia wiki URL prefix
URL_PREFIX = 'https://bulbapedia.bulbagarden.net/';
EP_PREFIX = 'wiki/EP';

# data folder webpages
EP_WEBPAGE_DEST = '../data/webpages/episodes/';

# files to write to
RAW_TEXT_FILE = '../data/data';
ANNOTATED_TEXT_FILE = '../data/data_annotated';
DESCRIPTORS_FILE = '../data/descriptors';
LABELED_DESCRIPTORS_FILE = '../data/descriptors_labeled';
RANDOM_LABELED_CORRECTED_DESCRIPTORS_FILE = '../data/random_descriptors_corrected_labeled';
LABELED_CORRECTED_DESCRIPTORS_FILE = '../data/descriptors_labeled_corrected';

TRAINING_DATA_SELF_FILE = '../data/training_data_self';

# proportion of the entities to construct vectors for
TRAINING_SET_SIZE_PER_LABEL = 100;

# proportion of the autolabeled data to use as the training set
TRAINING_SET_PROP = 0.8;

def create_shallow_pivot_dict(pivots):
    pivot_dict = {};
    for pivot in pivots:
        pivot_dict[pivot] = [pivot];

    return pivot_dict;


# pronouns
SUBJECT_PRONOUNS = ['he', 'she', 'it', 'they'];
subject_pronouns_pivots = create_shallow_pivot_dict(SUBJECT_PRONOUNS);
OBJECT_PRONOUNS = ['him', 'her', 'it', 'them'];
object_pronouns_pivots = create_shallow_pivot_dict(OBJECT_PRONOUNS);
POSSESSIVE_ADJECTIVES = ['his', 'her', 'its', 'their'];
possessive_adjectives_pivots = create_shallow_pivot_dict(POSSESSIVE_ADJECTIVES);
POSSESSIVE_PRONOUNS = ['his', 'hers', 'its', 'theirs'];
possessive_pronouns_pivots = create_shallow_pivot_dict(POSSESSIVE_PRONOUNS);
REFLEXIVE_PRONOUNS = ['himself', 'herself', 'itself', 'themselves'];
reflexive_pronouns_pivots = create_shallow_pivot_dict(REFLEXIVE_PRONOUNS);

PIVOT_CONJ_FILE = 'pivot_conjs';

ACTOR = 1;
TARGET = -1;

TEMPLATE_VECTOR = {};

directions = [ACTOR, TARGET];

verb_pivots = json.load(open('pivot_conjs'));

instances = [];

class Instance():
    """
    Initialize this Instance with the given context (containing sentence),
    label, and construct this instance's vector.

    _descriptor - the descriptor that generated this instance
    _context - the sentence in which the descriptor was found
    _descriptor_pos - the index of the match to descriptor in the context; 0
    unless there are more than one matches
    _label - the label of this instance
    """
    def __init__(self, _descriptor, _descriptor_pos, _context, _label):
        self.descriptor = _descriptor;
        self.descriptor_pos = _descriptor_pos;
        _context = re.sub(r'[^\w\s\'-]',' ',_context).lower();
        self.context = _context;
        self.label = _label;
        self.vector = {};
        self.set_vector(verb_pivots);
        self.set_vector(subject_pronouns_pivots);
        self.set_vector(object_pronouns_pivots);
        self.set_vector(possessive_adjectives_pivots);
        self.set_vector(possessive_pronouns_pivots);
        self.set_vector(reflexive_pronouns_pivots);

    def get_label(self):
        return self.label;

    def get_descriptor(self):
        return self.descriptor;

    def get_vector_dict(self):
        return self.vector;

    def get_vector(self):
        # sort alphabetically
        temp = [v for k, v in sorted(self.vector.items())];

        vectorized = [];
        for entry in temp:
            vectorized += [v for k, v in sorted(entry.items())];

        return vectorized;

    """
    Sets this instance's vector by searching for words in the context and
    identifying them as acting or targeting words.
    E.g., if the instance is "Bulbasaur" in the sentence "Bulbasaur uses Vine
    Whip.", "uses" is an acting pivot. On the other hand, if the instance is 
    "Vine Whip" in the sentence "Bulbasaur uses Vine Whip", "uses" is a
    targeting pivot.
    """
    def set_vector(self, pivots):
        for pivot in pivots:
            if pivot not in self.vector:
                # there are two entries per pivot; one set if this pivot is
                # used as an action this descriptor performs in this context
                # (ACTOR), and another set if this action is performed on this
                # descriptor in this context (TARGET)
                self.vector[pivot] = {ACTOR: 0, TARGET: 0};
            
        text_dirs = {};

        text_dirs[ACTOR] = self.context[self.descriptor_pos \
                + len(self.descriptor):].split(' ');
        text_dirs[ACTOR] = [x for x in text_dirs[ACTOR] if x];

        text_dirs[TARGET] = self.context[0:self.descriptor_pos].split(' ');
        text_dirs[TARGET] = [x for x in text_dirs[TARGET] if x];

        #print('text_dirs[ACTOR] ' + str(text_dirs[ACTOR]));
        #print('text_dirs[TARGET] ' + str(text_dirs[TARGET]));

        conjs = [];
        for pivot in pivots:
            conjs += pivots[pivot];

        # go left and right
        for direction in directions:
            words = text_dirs[direction];

            # current word index
            c_i = 0;

            if direction == TARGET:
                # going backward; start at last word
                c_i = len(words) - 1;
            elif direction == ACTOR:
                # going foward; start at first word
                c_i = 0;

            # stop after leaving the sentence
            while (c_i >= 0) and (c_i <= (len(words) - 1)):
                # extract this word
                word = words[c_i];

                # this word is a conjugation of the pivot
                if word in conjs:
                    # use the key as the found pivot in this direction
                    found = [k for k,v in pivots.items() if word in v][0];

                    self.vector[found][direction] = 1;

                    # TODO may want to consider subsequent matches
                    break;

                # go to next word
                c_i += direction;

