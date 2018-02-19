# File: self_training_set_constructor.py 
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen
# Created: 31/01/2018
import re;
import random;

from constants import *;

print("Reading file...");

# get all instances from file
instance_strings = [];
with open(INSTANCE_FILE) as f:
    instance_strings = f.read().splitlines();

print("Initializing mapping...");
# to hold mapping from labels to all instance objects of those labels
labels_to_instances = {};
for label in label_nums:
    labels_to_instances[label] = [];
    
print("Creating instances...");
i = 0;
for instance_string in instance_strings:
    print("Indexing instance: " + str(i) + '/' + str(len(instance_strings)));
    instance_string_split = instance_string.split('\t');
    #descriptor_string = instance_string_split[0];
    label_string = instance_string_split[1];
    #pos = int(instance_string_split[2]);
    #sentence_string = instance_string_split[3];

    # create a new Instance for this descriptor
    # instance = Instance(descriptor_string, pos, sentence_string, label_string);

    labels_to_instances[label_string].append(i);
    i += 1;

print("Creating training data...");
labels_to_instances_random = {};
for label in label_nums:
    labels_to_instances_random[label] = labels_to_instances[label].copy();
    random.shuffle(labels_to_instances_random[label]);

for i in range(TRAINING_SET_SIZE_PER_LABEL):
    print("Processing instance: " + str(i + 1) + "/" \
        + str(TRAINING_SET_SIZE_PER_LABEL));
    l_i = 0;
    for label in label_nums:
        print("\tProcessing label: " + str(l_i + 1) + "/" \
            + str(len(label_nums)));
        inst_list = labels_to_instances_random[label];
        num_inst = len(inst_list);

        if i >= len(inst_list):
            print("[WARNING] No remaining instances for label: " + label);
        else:
            instance_string = instance_strings[inst_list[i]];
            instance_string_split = instance_string.split('\t');
            descriptor_string = instance_string_split[0];
            label_string = instance_string_split[1];
            pos = int(instance_string_split[2]);
            sentence_string = instance_string_split[3];
            instance = Instance(descriptor_string, pos, sentence_string, label_string);
            instances.append(instance);

        l_i += 1;

data_lines_to_write = [];
# set strings for instances
for instance in instances:
    line = '';
    line += instance.get_descriptor() + '\t' + instance.get_label() + '\t';
    for entry in instance.get_vector():
        line += str(entry) + ' ';
    line = line[0:-1];
    line += '\n';
    data_lines_to_write.append(line);

random.shuffle(data_lines_to_write);

# string containing data to be written to file
file_data = '';
file_data += str(len(instances[0].get_vector())) + '\n';

# set string to write data to file
for line in data_lines_to_write:
    file_data += line;

with open(TRAINING_DATA_SELF_FILE, 'w') as file:
  file.write(file_data);
