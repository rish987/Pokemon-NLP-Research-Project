# Created: 31/01/2018
import enchant;

from constants import *;

# English dictionary
j = enchant.Dict('en_US');

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


descriptors = [];
with open(DESCRIPTORS_FILE) as f:
    descriptors = f.read().splitlines();

print(descriptors);
