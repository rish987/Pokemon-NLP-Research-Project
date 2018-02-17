# File: pivot_conj_dict_generator.py 
# Author(s): Rishikesh Vaishnav, TODO
# Created: 15/02/2018
import json;
from constants import *;

# load dictionary object
d = json.load(open('dictionary.json'));

# load raw data
filedata = '';
with open(RAW_TEXT_FILE, 'r') as file :
  filedata = file.read();

# to store mapping from verbs to their relevant conjugations
pivot_to_conjs = {};

i = 0;

num_words = len(d);

# go through all dictionary words
for word in d:
    print(str(i) + '/' + str(num_words));
    # extract all definitions of this word
    defs = d[word]['definitions'];

    # all of the different parts of speech of this word
    pos_list = [defs[x]['part_of_speech'] for x in \
        range(len(defs))]

    # this word can be interpreted as a verb
    if ('verb' in pos_list):
        # get all possible conjugations of this verb
        conjs = get_conjs(word);

        # go through all conjugations
        for conj in conjs:
            # this conjugation appears in the data
            if (len(re.findall(r'\b%s\b' % conj.lower(), \
                filedata.lower())) > 0):
                # create a new entry for this conjugation's originating word,
                # associating it with all of its conjugations
                pivot_to_conjs[word] = conjs;

print(pivot_to_conjs);
