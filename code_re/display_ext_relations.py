# File: display_ext_relations.py 
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen
# Created: 08/06/2018
# Displays relations extracted from triples in training_instance_finder.py

import pickle ;
from relation_templates import relations;
from constants import *;

with open(RELATION_TRIPLES_FILE, 'rb') as f:
    rels_to_rel_triples = pickle.load(f);

relation_nums = [0] + list(relations.keys())
for relation in relation_nums:
    print("Relation " + str(relation));
    for triple in rels_to_rel_triples[relation]:
        print("\t" + triple);
