# File: training_instance_finder.py
# Description: Extracts training instances for possible relations between
#              entities.
SUBJECT = 1
OBJECT = 3
DISTANCE_WEIGHT = 0
LENGTH_WEIGHT = 1

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

# location of raw triples
OPENIE_TRIPLES_FILE = "./data/openie_out" ;

# get triple file and split into lines
triple_filename = OPENIE_TRIPLES_FILE ;
triple_strs = '';
with open(triple_filename, 'r') as file:
    triple_strs = file.read().splitlines() ;

# finds the descriptor (if one exists) in the phrase and returns its label
def get_label (desc_phrase, direction):
    # to store tuples of the form (descriptor, descriptor-score), where each
    # score represents the confidence that this it the relevant descriptor in
    # the phrase
    desc_scores = []

    # iterate through ordered descriptors
    for descriptor in descriptors_ordered:
        r = re.compile(r'\b%s\b' % re.escape(descriptor))

        # to store tuples of the form (descriptor, edge-distance)
        desc_dists = []

        # go through all matches to the descriptor in the phrase
        for match in r.finditer(desc_phrase):
            position = match.span();
            distance = None;

            # should use distance from end of phrase
            if direction == SUBJECT:
                distance = len(desc_phrase) - 1 - position[1]
            # should use distance from beginning of phrase
            else:
                distance = position[0]

            desc_tuple = (descriptor, distance)
            desc_dists.append(desc_tuple)

        # sort descriptors by distance
        desc_dists_sorted = sorted(desc_dists, key=lambda x: x[1])

        # a descriptor was found
        if (len(desc_dists_sorted) > 0):
            # only consider the closest one
            closest_desc = desc_dists_sorted[0];
            score = (closest_desc[1] * (-1) * DISTANCE_WEIGHT) + \
                (len(closest_desc[0]) * LENGTH_WEIGHT)

            desc_scores.append((descriptor, score));
        # no matches found
        else:
            continue;

    # return the label of the descriptor of the highest score
    sorted_desc = sorted(desc_scores, key=lambda x: x[1])
    if (len(sorted_desc) != 0):
        return descriptors_to_labels[sorted_desc[-1][0]];
        
    # no descriptor was found in the phrase
    return None ;

# extracts the relevant keyword from the given action phrase if there is a
# keyword, other wise returns None
def get_keyword(action):
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
                r = re.compile(r'\b%s\b' % re.escape(keyword));
                # search only over middle verb portion of triple
                matches = list(r.finditer(action));

                # if anything was found at all, record it
                if (len(matches) > 0):
                    num_keywords += 1 ;

                    match = matches[0] ;

                    # position of first instance of this keyword
                    keyword_pos = match.span()[0] + 1;
                    keyword_positions[keyword] = keyword_pos ;

    # finish looping over all keywords

    # no keywords found
    if (num_keywords == 0):
        return None;

    # calculate confidence as a function of the number of keywords found
    # TODO: actually calculate instead of just nullifying triple
    if(num_keywords > 1):
        first_keyword_confidence = 0 ;
    else:
        first_keyword_confidence = 1;

    # sort by position in increasing order
    keyword_positions_ordered = sorted(keyword_positions.items(), \
        key=lambda x: x[1]) ;

    # keyword for this triple is the earliest keyword
    first_keyword = keyword_positions_ordered[0][0] ;

    # confident the first keyword is the relevant keyword
    if (first_keyword_confidence > 0.5):
        return first_keyword;

    # could not extract keyword
    return None;

# --- extract descriptor labels and relevant keywords from triples, and use
# these to classify them as indicative of specific relations ---

triple_num = 1;
# iterate through triples, looking for the keywords and corresponding pairs

# initialize empty lists to hold found triples
for relation in relations:
    rels_to_rel_triples[relation] = [] ;

# include a "None" relation
rels_to_rel_triples[0] = [];

#for triple_str in triple_strs[350:400]:
for triple_str in triple_strs:
    # split triple into subject, action, object
    triple = triple_str.split('\t')[1:];
    # TODO: eliminate triples that have wildly long subject or object

    print("On triple " + str(triple_num) + " out of " + \
        str(len(triple_strs)));
    print("\t" + triple_str);

    triple_num += 1;

    # extract relevant info from this triple
    subject_ext = get_label(triple[0], SUBJECT);
    object_ext = get_label(triple[2], OBJECT);
    keyword_ext = get_keyword(triple[1]);

    print('\t' + str(subject_ext), keyword_ext, object_ext);
    #print(keyword_ext);

    # --- determine relation of triple ---
    # tuple of labels for subject and object
    label_tup = (subject_ext, object_ext);
    relations_ext = [r for r in relations if \
                (label_tup in relations[r][FORWARD_PAIRS_IDX] and 
                keyword_ext in relations[r][FORWARD_WORDS_IDX])\
                or\
                (label_tup in relations[r][BACKWARD_PAIRS_IDX] and 
                keyword_ext in relations[r][BACKWARD_WORDS_IDX])];

    # no relations were detected, so classify this as a "None" relation
    if (len(relations_ext) == 0):
        relations_ext.append(0);
    # ---

    print("\tClassifications: " + str(relations_ext));
    # append rels_to_rel_triples
    for relation in relations_ext:
        rels_to_rel_triples[relation].append(triple_str);

    # clear triple file
    with open(RELATION_TRIPLES_FILE, 'wb') as file:
        file.close();
    # write lists of triples to file
    with open(RELATION_TRIPLES_FILE, 'wb') as file:
        pickle.dump(rels_to_rel_triples, file);
# ---
