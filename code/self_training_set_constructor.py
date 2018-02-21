# File: self_training_set_constructor.py 
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen
# Created: 31/01/2018
import re;
import random;

from constants import *;

"""
Returns a list of instance strings and a mapping from labels to the indices of 
the instance strings that have that label.
"""
def get_labels_to_instances():
    # get all instance strings from file
    instance_strings = [];
    with open(INSTANCE_FILE) as f:
        instance_strings = f.read().splitlines();

    # initialize mapping from labels to indices of all instance lines for those
    # labels
    labels_to_instances = {};
    for label in label_nums:
        labels_to_instances[label] = [];
        
    # assign labels_to_instances
    for i in range(len(instance_strings)):
        instance_string = instance_strings[i];
        instance_string_split = instance_string.split('\t');

        # extract this label and add this instace line's index to this label's
        # list of instance lines
        label_string = instance_string_split[1];
        labels_to_instances[label_string].append(i);

    ret_dict = { \
    "instance_strings": instance_strings, \
    "labels_to_instances": labels_to_instances \
    }
    return ret_dict;

"""
Create a processable training set an write it to file.
"""
def self_training_set_constructor(instance_strings, labels_to_instances, d):
    print("Creating training data...");

    # create a mapping from labels to instance indices with the instance
    # indices in each list randomized
    labels_to_instances_random = {};
    for label in label_nums:
        labels_to_instances_random[label] = labels_to_instances[label].copy();
        random.shuffle(labels_to_instances_random[label]);

    instances = [];

    # iterate a number of times equal to the size the training set should be
    # per label
    for i in range(TRAINING_SET_SIZE_PER_LABEL):
        print("Processing instances for labels: " + str(i + 1) + "/" \
            + str(TRAINING_SET_SIZE_PER_LABEL));
        
        # the current label index
        l_i = 0;

        # go through all labels
        for label in label_nums:
            #print("\tProcessing instance for label: " + str(l_i + 1) + "/" \
            #    + str(len(label_nums)));

            # extract list of instance string indices for this label
            inst_list = labels_to_instances_random[label];
            num_inst = len(inst_list);

            # have already used up all instances for this label
            if i >= num_inst:
                print("[WARNING] No remaining instances for label: " + label);
            # some instances of this label have not been used yet
            else:
                # extract this instance string and split it by tabs
                instance_string = instance_strings[inst_list[i]];
                instance_string_split = instance_string.split('\t');

                # extract descriptor, label, position, and sentence
                descriptor_string = instance_string_split[0];
                label_string = instance_string_split[1];
                pos = int(instance_string_split[2]);
                sentence_string = instance_string_split[3];

                # create a new instance for this, and add to list of instances
                instance = Instance(descriptor_string, pos, sentence_string, \
                    label_string, d);
                instances.append(instance);

            l_i += 1;

    data_lines_to_write = [];

    # set data strings for instances
    for instance in instances:
        line = '';
        line += instance.get_descriptor() + '\t' + instance.get_label() + '\t';
        for entry in instance.get_vector():
            line += str(entry) + ' ';
        line = line[0:-1];
        line += '\n';
        data_lines_to_write.append(line);

    # randomly shuffle all data strings
    random.shuffle(data_lines_to_write);

    # string containing data to be written to file
    file_data = '';
    file_data += str(len(instances[0].get_vector())) + '\n';

    # set string containing data to write to file by combining all data lines,
    # separating with newlines
    for line in data_lines_to_write:
        file_data += line;

    # clear training data file
    with open(TRAINING_DATA_SELF_FILE, 'w') as file:
      file.close();

    # write training data to file
    with open(TRAINING_DATA_SELF_FILE, 'w') as file:
      file.write(file_data);
