# File: training_instance_finder.py
# Description: Extracts training instances for possible relations between
#              entities.

# constants to index into dictionaries
FORWARD_WORDS_IDX = 0 ;
BACKWARD_WORDS_IDX = 1 ;
FORWARD_PAIRS_IDX = 2 ;
BACKWARD_PAIRS_IDX = 3 ;

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
