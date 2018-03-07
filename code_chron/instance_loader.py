# File: instance_loader.py 
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen
# Created: 06/03/2018
from constants import *;
import sys
sys.path.insert(0, 'objects')
from InstanceFinder import *;

LABELED_DESCRIPTORS_FILE = 'data/descriptors_labeled';

# load strings for each labeled descriptor
descriptor_and_label_strings = [];
with open(LABELED_DESCRIPTORS_FILE, 'r') as f:
    descriptor_and_label_strings = f.read().splitlines();

# to hold list of tuples for descriptors and their labels
descriptors_and_labels = [];

# go through all descriptor and label strings
for descriptor_and_label_string in descriptor_and_label_strings:
    descriptor_and_label_split = descriptor_and_label_string.split('\t');
    label_string = descriptor_and_label_split[0];
    descriptor_string = descriptor_and_label_split[1];

    # add tuple for this descriptor and label
    descriptors_and_labels.append((descriptor_string, label_string));

# go through all episodes
for ep_num in range(1, NUM_EPS + 1):
    print('Processing episode: ' + str(ep_num) + '/' + \
        str(NUM_EPS));
    # get text for this episode
    text_filename = TEXT_FOLDER + (EP_NUMBER_FORMAT % ep_num);
    text = '';
    with open(text_filename, 'r') as text_file:
        text = text_file.read();

    # open file to write instance to
    instances_filename = INSTANCES_FOLDER + (EP_NUMBER_FORMAT % ep_num);

    # clear instances file
    with open(instances_filename, 'w') as instances_file:
        instances_file.close();

    descriptor_i = 0;
    # go through all descriptors and labels
    for descriptor_and_label in descriptors_and_labels:
        print('\tProcessing descriptor: ' + str(descriptor_i + 1) + '/' + \
            str(len(descriptors_and_labels)));
        descriptor = descriptor_and_label[0];
        label = descriptor_and_label[1];
        finder = InstanceFinder(descriptor, label, text, instances_filename);

        # find and write instances
        finder.find_instances();
        finder.write_instances();

        descriptor_i += 1;
