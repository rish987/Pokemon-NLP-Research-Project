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
INSTANCE_FILE = '../data/instances';

# proportion of the entities to construct vectors for
TRAINING_SET_SIZE_PER_LABEL = 150;

# proportion of the autolabeled data to use as the training set
TRAINING_SET_PROP = 0.5;

# weight for distance of pivot from descriptor
D_WEIGHT = 0.9;

# weight for number of pivots found from descriptor
# N_WEIGHT = 0.1;
N_WEIGHT = float(1) - D_WEIGHT;

def create_shallow_pivot_dict(pivots):
    pivot_dict = {};
    for pivot in pivots:
        pivot_dict[pivot] = [pivot];

    return pivot_dict;

sentence_regex = r'[^.\?\!]*[^A-Za-z]%s(?:[^A-Za-z\.\?\!][^.\?\!]*)?[\.\?\!]';
descriptor_regex = r'[^A-Za-z]%s[^A-Za-z]';

class TSDescriptor():
    def __init__(self, _descriptor, _label, _filedata):
        self.descriptor = _descriptor;
        self.label = _label;
        self.instances = [];
        self.instance_ind = -1;
        self.filedata = _filedata;
        self.got_instances = False;

    def get_instances(self):
        return self.instances;

    def set_instances(self):
        # search for all matches to descriptor, and also grab surrounding words
        # in the sentence TODO may not always grab entire sentence, e.g. "Mr.
        # Mime" or "A.J." somewhere in the sentence will throw it off
        all_found = re.findall( sentence_regex % re.escape(self.descriptor), 
            self.filedata);
        if len(all_found) == 0:
            print("\tNO MATCH FOUND");
            return -1;

        for found in all_found:
            # print('SENTENCE: ' + found);
            r = re.compile(descriptor_regex % re.escape(self.descriptor));
            iterator = r.finditer(found)
            for match in iterator:
                descriptor_pos = match.span()[0] + 1;
                # print('\tMatch at: ' + str(descriptor_pos))
                self.instances.append(Instance(self.descriptor, \
                    descriptor_pos, found, self.label));

        self.got_instances = True;

        return 1;

    def rem_instances(self):
        return (not self.got_instances) or ((self.instance_ind + 1) \
            < len(self.instances));

    def get_next_instance(self):
        if not self.got_instances:
            result = self.set_instances();
            if result == -1:
                return -1;
        if not self.rem_instances():
            return None;
        self.instance_ind += 1;
        return self.instances[self.instance_ind];

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
ETC = ['a', 'as', 'at', 'about', 'after', 'before', 'behind', 'below',\
        'but', 'by', 'for', 'from', 'in', 'into', 'like', 'of', 'off', 'on',\
        's', 'onto', 'over', 'since', 'than', 'through', 'to', 'under',\
        'until', 'up', 'upon', 'the',  'with', 'without'];
etc_pivots = create_shallow_pivot_dict(ETC);

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
        _context = _context.replace('\n', '');
        self.context = _context;
        self.label = _label;
        self.vector = {};
        self.set_vector(verb_pivots);
        self.set_vector(subject_pronouns_pivots);
        self.set_vector(object_pronouns_pivots);
        self.set_vector(possessive_adjectives_pivots);
        self.set_vector(possessive_pronouns_pivots);
        self.set_vector(reflexive_pronouns_pivots);
        self.set_vector(etc_pivots);

    def get_label(self):
        return self.label;

    def get_descriptor(self):
        return self.descriptor;

    def get_vector_dict(self):
        return self.vector;

    def get_descriptor_pos(self):
        return self.descriptor_pos;

    def get_context(self):
        return self.context;

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

        passive = False;

        #if (len(text_dirs[TARGET]) > 0) and \
        #    (text_dirs[TARGET][len(text_dirs[TARGET]) - 1] == 'by') and \
        #    (len(text_dirs[ACTOR]) == 0):
        #    passive = True;

        #if (len(text_dirs[TARGET]) > 0) and \
        #    (text_dirs[TARGET][len(text_dirs[TARGET]) - 1] == 'by'):
        #    passive = True;

        # go left and right
        for direction in directions:
            words = text_dirs[direction];

            # current word index
            c_i = 0;

            # number of pivots found
            num_found = 0;

            # distance from current word
            d_i = 0;

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

                    # weighted value for distance
                    d_weighted = D_WEIGHT * (float(1) / float(d_i + 1));

                    # weighed value for number found
                    n_weighted = N_WEIGHT * (float(1) / float(num_found + 1));

                    direction_to_set = direction;

                    #if passive and (direction == TARGET):
                    #    direction_to_set = -direction_to_set;

                    self.vector[found][direction_to_set] = d_weighted \
                        + n_weighted;

                    num_found += 1;

                # go to next word
                c_i += direction;

                d_i += 1;
