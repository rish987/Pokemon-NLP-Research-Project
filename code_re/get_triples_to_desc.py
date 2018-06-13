# File: get_triples_to_desc.py 
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen
# Created: 13/06/2018
from constants import *;
import pickle;

# mapping from triples to their descriptor tuples
triples_to_desc_tups = {};

triple_i = 0;

triples = get_raw_triples();

# go through all triples
for triple in triples:
    print("on triple: " + str(triple_i + 1) + "/" + str(len(triples)));
    desc_tup = (get_desc(triple[0]), get_desc(triple[2]));
    print(desc_tup);
    triples_to_desc_tups[triple] = desc_tup;
    triple_i += 1;

# write lists of triples to file
with open(TRIPLES_TO_DESC_TUPS_FILE, 'wb') as file:
    pickle.dump(triples_to_desc_tups, file);
