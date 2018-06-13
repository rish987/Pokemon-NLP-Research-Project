# File: keyword_finder.py 
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen
# Created: 13/06/2018
# Description: An interactive program that finds forwards/backwards keywords and
# forwards/backwards descriptor label pairs for a certain relation. 
from constants import *;
import re;
import pickle;
from difflib import SequenceMatcher;

keywords = [];

triples = get_raw_triples();

# list of triples that have not yet been classified
unknown_triples = triples;

# list of triples that are known to imply this relation
valid_triples = [];

# list of triples that are known to not imply this relation
invalid_triples = [];

with open(TRIPLES_TO_DESC_TUPS_FILE, 'rb') as f:
    triples_to_desc_tups = pickle.load(f);

def correct_triples(triple_list):
    global unknown_triples;
    global valid_triples;
    global invalid_triples;

    # - display all triples, marked with a number - 
    triple_i = 0;
    nums_to_triples = {};
    for triple in triple_list:
        nums_to_triples[triple_i] = triple;
        print(str(triple_i) + ": " + str(triple));
        triple_i += 1;
    # - 

    # - separate correct/incorrect triples -
    # get list of numbers of incorrect triples
    bad_nums_str = input("Enter space-separated list of incorrect triples: ");

    bad_nums = [int(x) for x in bad_nums_str.split(' ') if x != ""];

    # all triples in nums_to_triples have been manually classified, so mark
    # them as known triples
    for triple in nums_to_triples.values():
        unknown_triples.remove(triple);

    #separate valid and invalid triples
    for bad_num in bad_nums:
        triple_to_remove = nums_to_triples[bad_num];
        invalid_triples.append(triple_to_remove);
        del nums_to_triples[bad_num];
    valid_triples += nums_to_triples.values();
    # - 

# initialize the program with a known keyword
init_keyword = input("Enter initialization keyword: ");

while(True):
    # - find all unknown triples containing the initialization keyword in the
    # action -
    init_keyword_triples = [];
    for triple in unknown_triples:
        found = re.search(r'\b%s\b' % re.escape(init_keyword), triple[1]);
        if (found != None):
            init_keyword_triples.append(triple);
    # -

    correct_triples(init_keyword_triples);
    triple_i = 0;

    # - find all unknown triples with matching descriptors as those of the valid
    # triples -
    # to store mapping from descriptor tuples to triples containing those
    # descriptors on either side
    desc_tup_to_triples = {};
    # go through all valid triples
    for triple in valid_triples:
        desc_tup = triples_to_desc_tups[triple];
        # there are two descriptors and there isn't already an entry for this
        # tuple
        if (desc_tup[0] != None) and (desc_tup[1] != None) and \
            (desc_tup not in desc_tup_to_triples):
            # find all unknown triples with this descriptor tuple
            desc_tup_to_triples[desc_tup] = [t for t in unknown_triples \
                    if triples_to_desc_tups[t] == desc_tup];

    # get list of all triples
    desc_tup_triples = [x for tup_trips in desc_tup_to_triples.values() \
        for x in tup_trips];
    # - 

    correct_triples(desc_tup_triples);

    # - extract keywords from valid list -
    # mapping from substring to the number of times it was seen in common between
    # two distinct valid triples
    substring_to_commonality_count = {};

    # go through all distrinct pairs of triples, looking at their actions
    for triple_i1 in range(len(valid_triples)):
        action_1 = valid_triples[triple_i1][1].lower();
        for triple_i2 in range(triple_i1 + 1, len(valid_triples)):
            action_2 = valid_triples[triple_i2][1].lower();

            match = SequenceMatcher(None, action_1, action_2).find_longest_match(\
                0, len(action_1), 0, len(action_2))

            largest_common_substring = action_1[match.a: match.a + match.size];
            if largest_common_substring not in substring_to_commonality_count:
                substring_to_commonality_count[largest_common_substring] = 1;
            else:
                substring_to_commonality_count[largest_common_substring] += 1;
    # - 

    sorted_substrings = sorted(\
            substring_to_commonality_count.items(), key=lambda x: x[1]);
    print([d for d in sorted_substrings if len(d[0]) > 2]);

    init_keyword = input("Enter the next keyword to iterate on: ");
    if init_keyword == "_quit":
        break;

