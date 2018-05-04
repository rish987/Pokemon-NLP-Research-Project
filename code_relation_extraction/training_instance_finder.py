# File: training_instance_finder.py
# Description: Extracts training instances for possible relations between
#              entities.
import re ;

from constants import * ;
from relation_templates import relations;

# to hold list of sentences containing a relationship
rel_sentences = [];

# maps relations to list of sentences found for that relation
rels_to_rel_sentences = {};

# --- get a dictionary mapping descriptors to their labels, and a list of
# ordered descriptors ---
# to hold mapping of descriptors to labels
descriptors_to_labels = {};

# open file and save lines to array
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

# constants to index into dictionaries
FORWARD_WORDS_IDX = 0 ;
BACKWARD_WORDS_IDX = 1 ;
FORWARD_PAIRS_IDX = 2 ;
BACKWARD_PAIRS_IDX = 3 ;

# direction indicators
FORWARD = 1 ;
BACKWARD = -1 ;

# location of text folder
TEXT_FOLDER = "./data/text/" ;

sentences = [];

def find_descriptors(sentence_dirs):
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


# go through all episodes
for ep_num in range(1, NUM_EPS + 1):
    # get text for this episode
    text_filename = TEXT_FOLDER + (EP_NUMBER_FORMAT % ep_num);
    text = '';
    with open(text_filename, 'r', encoding='utf8') as text_file:
        text = text_file.read();

    # --- get sentences of text ---

    # TODO replace naive '.'-delimited segmentation with more accurate
    # algorithm, such as HMM
    sentences += text.split('.');
# remove empty sentences
sentences = [sentence for sentence in sentences if len(sentence) > 0];

sentence_num = 1;
# iterate through sentences, looking for the keywords and corresponding pairs
for sentence in sentences:
    print("On sentence " + str(sentence_num) + " out of " + str(len(sentences)));
    sentence_num += 1;
    for pivot_direction in [FORWARD_WORDS_IDX, BACKWARD_WORDS_IDX]:
        # TODO: not just owns, iterate over list of relations
        for keyword in relations["owns"][pivot_direction]:
            r = re.compile(r'[^A-Za-z]%s[^A-Za-z]' % re.escape(keyword));
            iterator = r.finditer(sentence);

            # look forward and backward for the correct pair words
            # TODO: load label files in so that the program can identify that
            #       words with the correct labels are found before and after
            for match in iterator:
                keyword_pos = match.span()[0] + 1;

                text_dirs = {};

                # portion of the sentence string that occurs after the keyword
                text_dirs[FORWARD] = sentence[keyword_pos + len(keyword):] ;

                # portion of the sentence string that occurs before the keyword
                text_dirs[BACKWARD] = sentence[0:keyword_pos];
                
                descriptors_found = find_descriptors(text_dirs);
                
                label_tups_to_min_dist_tups = get_min_distance_label_pairs(descriptors_found);
               
                # finished filling out list of tuples    
                for label_tuple in label_tups_to_min_dist_tups:
                    label_pairs = relations["owns"][pivot_direction + 2]
                    if label_tuple in label_pairs:
                        if sentence not in rel_sentences:
                            rel_sentences.append(sentence);

print(rel_sentences);




                
