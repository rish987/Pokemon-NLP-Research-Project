# File: constants.py 
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen

# Created: 05/02/2018
import re;
import json;
import copy;

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
VECTORIZED_PROP = 0.2;

# proportion of the autolabeled data to use as the training set
TRAINING_SET_PROP = 0.7;

# pronouns
SUBJECT_PRONOUNS = ['he', 'she', 'it', 'they'];
OBJECT_PRONOUNS = ['him', 'her', 'it', 'them'];
POSSESSIVE_ADJECTIVES = ['his', 'her', 'its', 'their'];
POSSESSIVE_PRONOUNS = ['his', 'hers', 'its', 'theirs'];
REFLEXIVE_PRONOUNS = ['himself', 'herself', 'itself', 'themselves'];

PIVOT_CONJ_FILE = 'pivot_conjs';

ACTOR = 1;
TARGET = -1;

TEMPLATE_VECTOR = {};

directions = [ACTOR, TARGET];

pivots = json.load(open('pivot_conjs'));

for pivot in pivots:
    # there are two entries per pivot; one set if this pivot is used as an
    # action this descriptor performs in this context (ACTOR), and another set
    # if this action is performed on this descriptor in this context (TARGET)
    TEMPLATE_VECTOR[pivot] = {ACTOR: 0, TARGET: 0};

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
        _context = re.sub(r'[^\w\s]','',_context)
        self.context = _context;
        self.label = _label;
        self.vector = {};
        self.set_vector(TEMPLATE_VECTOR);

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
    E.g., if the instance is "Bulbasaur" in the sentence "Bublasaur uses Vine
    Whip.", "uses" is an acting pivot. On the other hand, if the instance is 
    "Vine Whip" in the sentence "Bulbasaur uses Vine Whip", "uses" is a
    targeting pivot.
    """
    def set_vector(self, template):
        # set template vector of this instance to fill
        self.vector.update(copy.deepcopy(template));

        text_dirs = {};

        text_dirs[ACTOR] = self.context[self.descriptor_pos \
                + len(self.descriptor):].split(' ');
        text_dirs[TARGET] = self.context[0:self.descriptor_pos].split(' ');

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

                    print(word);

                    self.vector[found][direction] = 1;

                    # TODO may want to consider subsequent matches
                    break;

                # go to next word
                c_i += direction;

