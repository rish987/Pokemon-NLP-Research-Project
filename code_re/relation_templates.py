#File: relation_templates.py
#Description: Stores information about the structure of predefined relations
# for use in automatically extracting training sentences.

# constants to index into dictionaries
FORWARD_WORDS_IDX = 0 ;
BACKWARD_WORDS_IDX = 1 ;
FORWARD_PAIRS_IDX = 2 ;
BACKWARD_PAIRS_IDX = 3 ;

# forward keywords related to the "owns" relation
owns_words_forward = ["own", "owns", "send out", "sends out", "recall", \
    "recalls", "withdraw", "withdraws", "call back", "calls back", "train", \
    "trains", "command", "commands", "order", "orders", "call for", \
    "calls for", "has", "choose", "chooses", "chose"] ;

# backward keywords related to the "owns" relation
owns_words_backward = ["obey", "obeys", "listen to", "listens to", \
    "return to", "returns to"] ;

# forward pairs related to the "owns" relation
owns_pairs_forward = [("person", "pokemon"), ("group", "pokemon")] ;

# backward pairs related to the "owns" relation
owns_pairs_backward = [("pokemon", "person"), ("pokemon", "group")] ;

# forward words related to the "uses" relation
uses_words_forward = ["use", "uses", "attack with", "attacks with", \
    "unleash", "unleashed", "fire", "fires", "fire off", "fires off"] ;

# backward words related to the "uses" relation
uses_words_backward = ["from", "used by"] ;

# forward pairs related to the "uses" relation
uses_pairs_forward = [("pokemon", "move")] ;

# backward pairs related to the "uses" relation
uses_pairs_backward = [("move", "pokemon")] ;

# information relevant to each relation: forward keywords, backward keywords,
#                                        forward pairs, backward pairs

# RELATION-LABEL NUMBER CORRESPONDENCES
# 0 - None
# 1 - Person Owns Pokémon
# 2 - Pokémon Has Move TODO: distinguish having and using
# 3 - Person In Settlement
# 4 - Person Calls for Move

relations = { \
    1 : \
    [owns_words_forward, owns_words_backward, \
    owns_pairs_forward, owns_pairs_backward], \

    2 : \
    [uses_words_forward, uses_words_backward, \
    uses_pairs_forward, uses_pairs_backward] \
    } ;
