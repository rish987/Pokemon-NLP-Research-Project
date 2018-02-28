# File: pivot_conj_dict_generator.py 
# Author(s): Rishikesh Vaishnav, TODO
# Created: 15/02/2018
import json;
import chardet;
from constants import *;
# using the NodeBox linguistics package for conjugation
import en;

"""
Return all conjugations of the given word.
"""
def get_conjs(word):
    conjs = [];

    try:
        # go through all persons
        for p in range(1, 4):
            conjs.append(en.verb.present(word, person=p));
            conjs.append(en.verb.past(word, person=p));

        conjs.append(en.verb.present_participle(word));
        conjs.append(en.verb.past_participle(word));
        conjs.append(word);
    # no entry for this word was found in NodeBox
    except KeyError:
        return [];

    # remove duplicates
    conjs = list(set(conjs));

    # remove blank strings
    if '' in conjs:
        conjs.remove('');

    return conjs;

# load dictionary object
d = json.load(open('dictionary.json'));

# load raw data
filedata = '';
with open(RAW_TEXT_FILE, 'r') as file :
  filedata = file.read();

filedata = filedata.lower();

global pivot_to_conjs;
# to store mapping from verbs to their relevant conjugations
pivot_to_conjs = {};

i = 0;

num_words = len(d);

def process_conjs(word):
    try:
	word.encode('ascii');
    except UnicodeEncodeError:
	return;

    # ignore this word if it has a space in it or cannot be converted to ascii
    if (' ' in word) or (not en.is_verb(word)):
        #print("could not process word: " + word);
        return;

    # extract all definitions of this word
    defs = d[word]['definitions'];

    # all of the different parts of speech of this word
    pos_list = [defs[x]['part_of_speech'] for x in range(len(defs))]

    # this word can be interpreted as a verb
    if ('verb' in pos_list):
        # get all possible conjugations of this verb
        conjs = get_conjs(word);

        # no matching verb was found
        if (len(conjs) == 0):
            # try again with 's' at the end (problem with NodeBox)
            conjs = get_conjs(word + 's');
            # no matching verb was found
            if (len(conjs) == 0):
                return;

            if word not in conjs:
                conjs.append(word);

        # go through all conjugations
        for conj in conjs:
            conj = conj.strip();
            # this conjugation appears in the data
            if (re.search(r'\b%s\b' % conj.lower(), \
                filedata) != None):
                # create a new entry for this conjugation's originating word,
                # associating it with all of its conjugations
                pivot_to_conjs[word] = conjs;

                # no need to search for the next conjugation
                break;

# go through all dictionary words
for word in d:
    i += 1;
    print(str(i) + '/' + str(num_words) + ': ' + word);
    process_conjs(word);

with open('pivot_conjs', 'w') as file:
     file.write(json.dumps(pivot_to_conjs));
