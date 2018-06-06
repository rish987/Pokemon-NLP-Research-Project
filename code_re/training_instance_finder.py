# File: training_instance_finder.py
# Description: Extracts training instances for possible relations between
#              entities.

import re ;
import pickle ;

from constants import * ;
from relation_templates import * ;

# maps relations to list of triples found for that relation
rels_to_rel_triples = {};

# --- get a dictionary mapping descriptors to their labels, and a list of
# ordered descriptors ---
# to hold mapping of descriptors to labels
descriptors_to_labels = {};

# open descriptor-to-label file and save lines to array
descriptors_labeled_file_lines = [];
with open(DESCRIPTORS_LABELED_FILE, 'r') as file:
    descriptors_labeled_file_lines = file.read().splitlines();

# construct dictionary mapping
for line in descriptors_labeled_file_lines:
    split = line.split('\t');
    label = split[0];
    descriptor = split[1];
    descriptors_to_labels[descriptor] = label;

# to hold descriptors ordered by length
descriptors_ordered = list(descriptors_to_labels.keys());

descriptors_ordered = \
    list(reversed(sorted(descriptors_ordered, key=lambda x: len(x))));
# ---

# direction indicators
FORWARD = 1 ;
BACKWARD = -1 ;

# location of raw triples
OPENIE_TRIPLES_FILE = "./data/openie_out/" ;

triples = [];

def find_descriptors(triple_dirs):
    descriptors_found = {};
    descriptors_found[FORWARD] = [];
    descriptors_found[BACKWARD] = [];
    
    for direction in [FORWARD, BACKWARD]:
        for descriptor in descriptors_ordered:
            r = re.compile(r'[^A-Za-z]%s[^A-Za-z]' % re.escape(descriptor));
            iterator = r.finditer(text_dirs[direction]);
            
            # add a (descriptor, position) tuple to the list of
            # descriptors in this direction for each match
            for desc_match in iterator:
                desc_pos = desc_match.span()[0] + 1;
                distance = None;
                if direction == FORWARD:
                    distance = desc_pos;
                else:
                    distance = (len(text_dirs[BACKWARD]) - desc_pos) - 1;
                descriptors_found[direction].append((descriptor, \
                    distance));
    return descriptors_found;


def get_min_distance_label_pairs(descriptors_found):
    # mapping from all observed label tuples around this keyword to
    # pairs of numbers where each number is the minimum
    # distance from the keyword to a label of this type in the
    # backwards and forwards directions, respectively
    label_tups_to_min_dist_tups = {};
    # go through all possible pairs of descriptors
    for forward_descriptor, forwards_dist in \
        descriptors_found[FORWARD]:
        for backward_descriptor, backwards_dist in descriptors_found[BACKWARD]:
            label_tup = (descriptors_to_labels[\
                    backward_descriptor], \
                    descriptors_to_labels[forward_descriptor]);


            if label_tup in label_tups_to_min_dist_tups:
                prev_backward_dist = \
                    label_tups_to_min_dist_tups[label_tup][0];
                prev_forward_dist = \
                    label_tups_to_min_dist_tups[label_tup][1];
                label_tups_to_min_dist_tups[label_tup] =\
                    (min(prev_backward_dist, backwards_dist),\
                     min(prev_forward_dist, forwards_dist));
            else:
                label_tups_to_min_dist_tups[label_tup] = \
                (backwards_dist, forwards_dist);
    return label_tups_to_min_dist_tups;


# get triple file and split into lines
triple_filename = OPENIE_TRIPLES_FILE ;
text_lines = '';
with open(triple_filename, 'r') as file:
    text_lines = file.read().splitlines() ;

# --- get triple from each line ---

for text_line in text_lines:
    # do not use confidence value
    triples += text_line.split('\t')[1:] ;

# remove empty triples
# TODO: eliminate triples that have wildly long subject or object
# triples = [triple for triple in triples if len(triple) > 0];

triple_num = 1;
# iterate through triples, looking for the keywords and corresponding pairs

# initialize empty lists to hold found triples
for relation in relations:
    rels_to_rel_triples[relation] = [] ;

for triple in triples:
    print("On triple " + str(triple_num) + " out of " + \
        str(len(triples)));

    triple_num += 1;

    # keyword tracking
    num_keywords = 0 ;
    keyword_positions = {} ;
    # confidence that the first keyword is the relevant keyword
    first_keyword_confidence = 0 ;

    for pivot_direction in [FORWARD_WORDS_IDX, BACKWARD_WORDS_IDX]:
        # iterate over all relations
        for relation in relations:

            # use specific relation to index into relation dictionary and get
            # word lists
            for keyword in relations[relation][pivot_direction]:
                r = re.compile(r'[^A-Za-z]%s[^A-Za-z]' % re.escape(keyword));
                # search only over middle verb portion of triple
                iterator = r.finditer(triple[1]);

                # if anything was found at all, record it
                if (len(iterator) > 0):
                    num_keywords += 1 ;

                    match = iterator[0] ;

                    # position of first instance of this keyword
                    keyword_pos = match.span()[0] + 1;
                    keyword_positions[keyword] = keyword_pos ;

    # finish looping over all keywords

    # calculate confidence as a function of the number of keywords found
    # TODO: actually calculate instead of just nullifying triple
    if(num_keywords > 1):
        first_keyword_confidence = 0 ;

    # sort by position in increasing order
    keyword_positions_ordered = sorted(keyword_positions.items(), \
        key=lambda x: x[1]) ;

    # keyword for this triple is the earliest keyword
    # TODO: add scaling based on confidence
    triple_keyword = keyword_positions_ordered[0][0] ;

    # put this triple in rels_to_rel_triples based on keyword
    # TODO: find out what relation it is, including looking at labels in
    # triple[0] and triple[2]

# write lists of triples to file
with open(RELATION_TRIPLES_FILE, 'wb') as file:
    pickle.dump(rels_to_rel_triples, file);
