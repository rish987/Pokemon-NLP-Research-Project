# File: constants.py 
# Author(s): Rishikesh Vaishnav, Jessica Lacovelli, Bonnie Chen

# Created: 05/02/2018
import re
import json

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

# proportion of the autolabeled data to use as the training set
TRAINING_SET_PROP = 0.7;

# matches a string, with leading and trailing characters
DESCRIPTOR_FORMAT_STRING = r'(?:\S+)?%s(?:\S+)?';

# starting regex
regex = DESCRIPTOR_FORMAT_STRING;

# number of surrounding words to match
NUM_SURR_WORDS = 1;

# matches any spaces or sequence of characters
WORD_FORMAT_SPACES = '\s+';
WORD_FORMAT_WORD = '\S+';

# matches any word before a match
WORD_FORMAT_BEFORE = WORD_FORMAT_WORD + WORD_FORMAT_SPACES;

# matches any word after a match
WORD_FORMAT_AFTER = WORD_FORMAT_SPACES + WORD_FORMAT_WORD;

# all parts of speech
POS_TERMS = ['adjective', 'noun', 'preposition', 'verb', 'adverb', 'pronoun', 'conjunction', 'interjection', 'article', 'none'];

# template for Descriptor POS vectors
POS_VECTOR_TEMPLATE = {};
for term in POS_TERMS:
    POS_VECTOR_TEMPLATE[term] = 0;

# go through all surrounding words to add to regex
for i in range(NUM_SURR_WORDS):
    # add word before
    regex = WORD_FORMAT_BEFORE + regex;
    regex = regex + WORD_FORMAT_AFTER;

class Descriptor():
    def __init__(self, _title, _label):
        self.title = _title;
        self.label = _label;
        self.predicted_label = None;
        self.pos_vector = POS_VECTOR_TEMPLATE.copy();

    def get_title(self):
        return self.title;

    def get_label(self):
        return self.label;

    def get_word_map(self):
        return self.word_map;

    def get_vector(self):
        return [self.pos_vector[w] for w in \
                sorted(self.pos_vector)];

    """
    Deconstructs the given string, and updates this Descriptor's word_map
    with the number of occurrences of each of the words in this string.
    """
    def add_words(self, string):
        # remove this descriptor from the string
        #string = re.sub((DESCRIPTOR_FORMAT_STRING + '\s+') % self.title, '', string);
        words = string.split(' ');
        for word in words:
            # remove leading or trailing punctuation
            words_found = re.findall(r'\w+', word);
            if len(words_found) > 0:
                word = re.findall(r'\w+', word)[0].lower();

                # ensure word is in english dictionary
                if word in d:
                    defs = d[word]['definitions'];

                    # all of the different parts of speech of this word
                    pos_list = [defs[x]['part_of_speech'] for x in \
                            range(len(defs))]

                    # add one to every entry in the pos vector with a matching
                    # pos
                    for pos in pos_list:
                        # pos defined for this definition
                        if len(pos) > 0:
                            if pos in self.pos_vector:
                                self.pos_vector[pos] += 1;
                            else:
                                #self.pos_vector['none'] += 1;
                                pass;
                else:
                    self.pos_vector['none'] += 1;
