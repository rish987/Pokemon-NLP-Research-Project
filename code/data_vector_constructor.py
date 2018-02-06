# Created: 31/01/2018
import enchant;
import re;

from constants import *;

# English dictionary
j = enchant.Dict('en_US');

# matches any punctuation
DESCRIPTOR_FORMAT_SPACES = '\s+';
DESCRIPTOR_FORMAT_WORD = '\S+';

# matches any word before a match
DESCRIPTOR_FORMAT_BEFORE = DESCRIPTOR_FORMAT_WORD + DESCRIPTOR_FORMAT_SPACES;

# matches any word after a match
DESCRIPTOR_FORMAT_AFTER = DESCRIPTOR_FORMAT_SPACES + DESCRIPTOR_FORMAT_WORD;


# number of surrounding words to match
NUM_SURR_WORDS = 2;

# string to match descriptor, in its plural forms as well (ending in 'es' or
# 's'), both separate and unseparate from other words
DESCRIPTOR_FORMAT_SEPARATE = r'(\b%s(?:e?s)?\b)';
DESCRIPTOR_FORMAT_UNSEPARATE = r'(%s(?:e?s)?)';

class Descriptor():
    def __init__(self, _title):
        self.title = _title;
        self.word_map = {};

    """
    Deconstructs the given string, and updates this Descriptor's word_map
    with the number of occurrences of each of the words in this string.
    """
    def add_words(self, string):
        words = string.split(' ');
        for word in words:
            # ensure word is in english dictionary
            if d.check(word):
                if word not in self.word_map:
                    self.word_map[word] = 0;

                self.word_map[word] += 1;


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
regex = r'%s';

# go through all surrounding words to add to regex
for i in range(NUM_SURR_WORDS):
    # add word before
    regex = DESCRIPTOR_FORMAT_BEFORE + regex;
    regex = regex + DESCRIPTOR_FORMAT_AFTER;

for descriptor_string in descriptor_strings:
    # search for all matches to descriptor, and also grab surrounding words
    all_found = re.findall( regex % \
            re.escape(descriptor_string), filedata);
    if len(all_found) == 0:
        print("descriptor: " + descriptor_string);
