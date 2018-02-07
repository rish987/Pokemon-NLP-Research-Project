# File: constants.py 
# Author(s): Rishikesh Vaishnav, Jessica Lacovelli, Bonnie Chen

# Created: 05/02/2018
import re
import enchant;

# English dictionary
d = enchant.Dict('en_US');

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
TRAINING_SET_PROP = 0.5;

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
        self.word_map = {};
        self.dictionary_vector = {};
        self.vector = [];

    def get_title(self):
        return self.title;

    def get_label(self):
        return self.label;

    def get_word_map(self):
        return self.word_map;

    def get_vector(self):
        return self.vector;

    """
    Deconstructs the given string, and updates this Descriptor's word_map
    with the number of occurrences of each of the words in this string.
    """
    def add_words(self, string):
        # remove this descriptor from the string
        string = re.sub((DESCRIPTOR_FORMAT_STRING + '\s+') % self.title, '', string);
        words = string.split(' ');
        for word in words:
            # remove leading or trailing punctuation
            words_found = re.findall(r'\w+', word);
            if len(words_found) > 0:
                word = re.findall(r'\w+', word)[0].lower();

                # ensure word is in english dictionary
                if d.check(word):
                    if word not in self.word_map:
                        self.word_map[word] = 0;

                    self.word_map[word] += 1;

    """
    Sets this descriptor's dictionary vector (the vector containing all words
    found over all descriptors), populates the relevant word entries with
    their corresponding counts, and sets up the vector representation of this
    descriptor.
    """
    def set_dictionary_vector(self, _dictionary_vector):
        self.dictionary_vector = _dictionary_vector.copy();
        for word in self.word_map:
            if word in self.dictionary_vector:
                self.dictionary_vector[word] = self.word_map[word];
        # TODO normalize ?
        self.vector = [self.dictionary_vector[w] for w in \
                sorted(self.dictionary_vector)];

    
