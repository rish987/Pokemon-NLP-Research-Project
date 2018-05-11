# File: relation_ranker.py 
# Author(s): Rishikesh Vaishnav, TODO
# Created: 17/04/2018
#
# Description: Ranks relation tuples based on frequency of occurrence in the
# list of relations extracted by OpenIE.
# TODO split tab-delimited areas by white space when parsing for labels
from constants import *;
import operator;

# to store mapping from relation tuple to frequency in OpenIE output
relation_tuples_to_freq = {};

for label_1 in descriptor_labels:
    for label_2 in descriptor_labels:
        relation_tuples_to_freq[(label_1, label_2)] = [0, []];

# to hold mapping of descriptors to labels and descriptors ordered by length
descriptors_to_labels, descriptors_ordered = get_dictionary_desc_to_labels() ;

openie_out_file_lines = [];
with open(OPENIE_OUTPUT_FILE, 'r') as file:
    openie_out_file_lines = file.read().splitlines();

for line in openie_out_file_lines:
    split = line.split('\t');
    subject_term = split[1];
    object_term = split[3];
    subj_in_desc_to_labels = False;
    subj_term_match = ''
    for descriptor in descriptors_ordered:
        if descriptor in subject_term:
            subj_in_desc_to_labels = True;
            subj_term_match = descriptor;
            break;

    obj_in_desc_to_labels = False;
    obj_term_match = ''
    for descriptor in descriptors_ordered:
        if descriptor in object_term:
            obj_in_desc_to_labels = True;
            obj_term_match = descriptor;
            break;
    if (subj_in_desc_to_labels) and \
        (obj_in_desc_to_labels):
        subj_obj_tuple = (descriptors_to_labels[subj_term_match],\
                descriptors_to_labels[obj_term_match]);
        relation_tuples_to_freq[subj_obj_tuple][0] += 1;
        relation_tuples_to_freq[subj_obj_tuple][1].append(\
                line.replace("\t", "|"));

sorted_relation_tuples_to_freq = \
        sorted(relation_tuples_to_freq.items(), key=lambda x: x[1][0]);
sorted_relation_tuples_to_freq.reverse();

file_str = '';

for relation_tuple, freq_list in sorted_relation_tuples_to_freq:
    file_str += relation_tuple[0] + " -> " + relation_tuple[1] + " (" \
            + str(freq_list[0]) + ")" + "\n";

    for text_relation in freq_list[1]:
        file_str += "\t" + text_relation + "\n";

with open(SORTED_TUPLES_FILE, 'w') as file:
    file.write(file_str);
