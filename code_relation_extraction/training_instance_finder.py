# File: training_instance_finder.py
# Description: Extracts training instances for possible relations between
#              entities.

import re ;

from constants import * ;

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

# forward keywords related to the "owns" relation
owns_words_forward = ["own", "owns", "send out", "sends out", "recall", \
    "recalls", "withdraw", "withdraws", "call back", "calls back", "train", \
    "trains", "command", "commands", "order", "orders", "call for", \
    "calls for"] ;

# backward keywords related to the "owns" relation
owns_words_backward = ["obey", "obeys", "listen to", "listens to", \
    "return to", "returns to"] ;

# forward pairs related to the "owns" relation
owns_pairs_forward = [("person", "pokemon"), ("group", "pokemon")] ;

# backward pairs related to the "owns" relation
owns_pairs_backward = [("pokemon", "person"), ("pokemon", "group")] ;

# information relevant to each relation: forward keywords, backward keywords,
#                                        forward pairs, backward pairs
relations = {"owns" : [owns_words_forward, owns_words_backward, \
    owns_pairs_forward, owns_pairs_backward]} ;

# go through all episodes
for ep_num in range(1, NUM_EPS + 1):
    print('Processing episode: ' + str(ep_num) + '/' + \
        str(NUM_EPS));
    # get text for this episode
    text_filename = TEXT_FOLDER + (EP_NUMBER_FORMAT % ep_num);
    text = '';
    with open(text_filename, 'r', encoding='utf8') as text_file:
        text = text_file.read();

    # --- get sentences of text ---

    # TODO replace naive '.'-delimited segmentation with more accurate
    # algorithm, such as HMM
    sentences = text.split('.');
    # remove empty sentences
    sentences = [sentence for sentence in sentences if len(sentence) > 0];

# iterate through sentences, looking for the keywords and corresponding pairs
for sentence in sentences:
    # TODO: not just owns, iterate over list of relations
    for keyword in owns_words_forward:
        r = re.compile("\b%s\b" % re.escape(keyword));
        iterator = r.finditer(found)

        # look forward and backward for the correct pair words
        # TODO: load label files in so that the program can identify that
        #       words with the correct labels are found before and after
        for match in iterator:
            keyword_pos = match.span()[0] + 1;

            text_dirs = {};

            # portion of the sentence string that occurs before the keyword
            text_dirs[FORWARD] = sentence[keyword_pos \
                    + len(self.descriptor):] ;

            # portion of the sentence string that occurs after the keyword
            text_dirs[BACKWARD] = sentence[0:keyword_pos];
