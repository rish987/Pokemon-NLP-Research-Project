# Created: 31/01/2018
import enchant;
import re;

from constants import *;

# English dictionary
d = enchant.Dict('en_US');

# English dictionary
j = enchant.Dict('en_US');

# matches any spaces or sequence of characters
WORD_FORMAT_SPACES = '\s+';
WORD_FORMAT_WORD = '\S+';

# matches a string, with leading and trailing characters
DESCRIPTOR_FORMAT_STRING = r'(?:\S+)?%s(?:\S+)?';

# matches any word before a match
WORD_FORMAT_BEFORE = WORD_FORMAT_WORD + WORD_FORMAT_SPACES;

# matches any word after a match
WORD_FORMAT_AFTER = WORD_FORMAT_SPACES + WORD_FORMAT_WORD;

# number of surrounding words to match
NUM_SURR_WORDS = 1;

# string to match descriptor, in its plural forms as well (ending in 'es' or
# 's'), both separate and unseparate from other words
DESCRIPTOR_FORMAT_SEPARATE = r'(\b%s(?:e?s)?\b)';
DESCRIPTOR_FORMAT_UNSEPARATE = r'(%s(?:e?s)?)';

class Descriptor():
    def __init__(self, _title):
        self.title = _title;
        self.word_map = {};
        self.dictionary_vector = {};
        self.vector = [];

    def get_word_map(self):
        return self.word_map;

    """
    Deconstructs the given string, and updates this Descriptor's word_map
    with the number of occurrences of each of the words in this string.
    """
    def add_words(self, string):
        print(string);
        # remove this descriptor from the string
        string = re.sub((DESCRIPTOR_FORMAT_STRING + '\s+') % self.title, '', string);
        words = string.split(' ');
        for word in words:
            # remove leading or trailing punctuation
            words_found = re.findall(r'\w+', word);
            if len(words_found) > 0:
                word = re.findall(r'\w+', word)[0].lower();

                print("Checking word: " + word); 

                # ensure word is in english dictionary
                if d.check(word):
                    print("\t+");
                    if word not in self.word_map:
                        self.word_map[word] = 0;

                    self.word_map[word] += 1;
                else:
                    print("\t-");

    """
    Sets this descriptor's dictionary vector (the vector containing all words
    found over all descriptors), populates the relevant word entries with
    their corresponding counts, and sets up the vector representation of this
    descriptor.
    """
    def set_dictionary_vector(self, _dictionary_vector):
        self.dictionary_vector = _dictionary_vector.copy();
        for word in self.word_map:
            self.dictionary_vector[word] = self.word_map[word];
        # TODO normalize
        self.vector = [self.dictionary_vector[w] for w in \
                sorted(self.dictionary_vector)];
        print(self.title);
        print('\t', self.vector);


descriptor_strings = [];
with open(DESCRIPTORS_FILE) as f:
    descriptor_strings = f.read().splitlines();

# to hold all descriptor objects
descriptors = [];

# load the raw data
filedata = None;
with open(RAW_TEXT_FILE, 'r') as file :
  filedata = file.read();

# starting regex
regex = DESCRIPTOR_FORMAT_STRING;

# go through all surrounding words to add to regex
for i in range(NUM_SURR_WORDS):
    # add word before
    regex = WORD_FORMAT_BEFORE + regex;
    regex = regex + WORD_FORMAT_AFTER;

for descriptor_string in descriptor_strings:
    print("descriptor: " + descriptor_string);
    # search for all matches to descriptor, and also grab surrounding words
    all_found = re.findall( regex % \
            re.escape(descriptor_string), filedata);
    descriptor = Descriptor(descriptor_string);
    if len(all_found) == 0:
        print("\tNO MATCH FOUND");

    for found in all_found:
        # pass the words on the the descriptor for it to add them to its
        # dictionary
        descriptor.add_words(found);

    descriptors.append(descriptor);

# template for descriptor vectors - will have one entry per unique surrounding
# word found in all of the descriptors
vector_template = {};

# populate vector_template
for descriptor in descriptors:
    for word in descriptor.get_word_map():
        if word not in vector_template:
            vector_template[word] = 0;

# set vectors for descriptors
for descriptor in descriptors:
    descriptor.set_dictionary_vector(vector_template);
