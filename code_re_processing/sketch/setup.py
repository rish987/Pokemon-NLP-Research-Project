# File: main.py 
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen
# Created: 29/05/2018
# Description:
#   Setup code for path correlation algorithm grapher.
from graph_params import Label, Descriptor, Relation;

# - IO parameters -
# filenames in which to find labels descriptors, and relations
LABEL_FILE_FILENAME = 'labels';
DESC_FILE_FILENAME = 'descriptors';
REL_FILE_FILENAME = 'relations';

# folder in which to find descriptors, labels, and relations (graph parameters)
GRAPH_PARAM_FOLDER = '../ex_graph_params/';
# -

"""
Returns a lists of Label, Descriptor and Relation objects using the relevant
files in the given folder.
"""
def load_graph_params(folder_name):
    # - read in string list of labels and construct Relation object list -
    # to store list of label strings
    labels_str = [];

    # open file where each line contains a label
    with open(folder_name + LABEL_FILE_FILENAME, 'r') as file:
        text = file.read();
        labels_str = text.splitlines();

    # to store list of Label objects
    labels = [];

    # go through all (label, label) pairs
    for label_str in labels_str:
        label = Label(label_str);

        # add a new Label object to the list
        labels.append(label);
    # -

    # - read in string list of descriptors and construct Descriptor 
    # object list -
    # to store list of (descriptor, label) string tuples
    descriptors_and_labels_str = [];

    # open file where each line contains a 'descriptor' and 'label' in the
    # format 'descriptor\tlabel'
    with open(folder_name + DESC_FILE_FILENAME, 'r') as file:
        text = file.read();
        text_lines = text.splitlines();
        text_lines_split = [x.split('\t') for x in text_lines];
        descriptors_and_labels_str = [(x[0], x[1]) for x in text_lines_split]


    # to store list of Descriptor objects
    descriptors = [];

    # go through all (descriptor, label) pairs
    for descriptor, label in descriptors_and_labels_str:
        # add a new Descriptor object to the list
        this_label = [x for x in labels if (x.get_name() == label)][0]
        descriptors.append(Descriptor(descriptor, this_label));
    # -

    # - read in string list of relations and construct Relation object list -
    # to store list of relation strings
    relations_str = [];

    # open file where each line contains a relation name
    with open(folder_name + REL_FILE_FILENAME, 'r') as file:
        text = file.read();
        relations_str = text.splitlines();

    # to store list of Relation objects
    relations = [];

    # go through all (relation, label) pairs
    for relation_str in relations_str:
        # add a new Relation object to the list
        relations.append(Relation(relation_str));
    # -

    return labels, descriptors, relations;
