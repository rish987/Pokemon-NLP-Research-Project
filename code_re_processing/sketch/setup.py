# File: main.py 
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen
# Created: 29/05/2018
# Description:
#   Setup code for path correlation algorithm grapher.
from graph_params import Label, Descriptor, Relation, RelationInstance;

# - IO parameters -
# filenames in which to find labels descriptors, and relations
LABEL_FILE_FILENAME = 'labels';
DESC_FILE_FILENAME = 'descriptors';
REL_FILE_FILENAME = 'relations';

# folder in which to find descriptors, labels, and relations (graph parameters)
GRAPH_PARAM_FOLDER = '../ex_graph_params/';
# -

"""
Returns a lists of Label, Descriptor, Relation, and RelationInstance 
objects using the relevant files in the given folder.
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
    # to store list of (descriptor, label, (optional coordinates)[x, y]) 
    # string tuples
    descriptors_and_labels_str = [];

    # is this a file containing coordinates?
    with_coords = False;

    # open file where each line contains a 'descriptor' and 'label' in the
    # format 'descriptor\tlabel'
    with open(folder_name + DESC_FILE_FILENAME, 'r') as file:
        text = file.read();
        text_lines = text.splitlines();
        text_lines_split = [x.split('\t') for x in text_lines];

        # determine if this is a file containing coordinates
        with_coords = (len(text_lines_split[0]) == 4);
        
        # this is a file containing coordinates
        if (with_coords):
            descriptors_and_labels_str = [(x[0], x[1], x[2], x[3]) for x in \
                text_lines_split];
        else:
            descriptors_and_labels_str = [(x[0], x[1]) for x in \
                text_lines_split];

    # to store list of Descriptor objects
    descriptors = [];

    # go through all (descriptor, label) pairs
    for tup in descriptors_and_labels_str:
        descriptor = tup[0];
        label = tup[1];

        # add a new Descriptor object to the list
        this_label = [x for x in labels if (x.get_name() == label)][0]
        if (with_coords):
            x = int(tup[2]);
            y = int(tup[3]);
            descriptors.append(Descriptor(descriptor, this_label, x, y));
        else:
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

    # - construct RelationInstance list -
    # to hold list of relation instances
    relation_instances = [];

    # go through all pairs of descriptors
    for descriptor_subj in descriptors:
        for descriptor_obj in descriptors:
            if descriptor_subj != descriptor_obj:
                # go through all relations
                for relation in relations:
                    relation_instances.append(RelationInstance(\
                        descriptor_subj,\
                        descriptor_obj, relation));
    # - 

    return labels, descriptors, relations, relation_instances;
