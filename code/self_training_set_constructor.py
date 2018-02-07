# File: self_training_set_constructor.py 
# Author(s): Rishikesh Vaishnav, Jessica Lacovelli, Bonnie Chen
# Created: 31/01/2018
import re;
import random;

from constants import *;

# string to match descriptor, in its plural forms as well (ending in 'es' or
# 's'), both separate and unseparate from other words
DESCRIPTOR_FORMAT_SEPARATE = r'(\b%s(?:e?s)?\b)';
DESCRIPTOR_FORMAT_UNSEPARATE = r'(%s(?:e?s)?)';

descriptor_and_label_strings = [];
with open(LABELED_CORRECTED_DESCRIPTORS_FILE) as f:
    descriptor_and_label_strings = f.read().splitlines();

# randomly shuffle strings
random.shuffle(descriptor_and_label_strings);

# write randomly shuffled strings and labels to file for use in other programs
randomized_file = '';
for string in descriptor_and_label_strings:
    randomized_file += string + '\n';
with open(RANDOM_LABELED_CORRECTED_DESCRIPTORS_FILE, 'w') as f:
    f.write(randomized_file);
    f.close();

# to hold all descriptor objects
descriptors = [];

# load the raw data
filedata = None;
with open(RAW_TEXT_FILE, 'r') as file :
  filedata = file.read();

last_descriptor_i = int(len(descriptor_and_label_strings) * TRAINING_SET_PROP);

for i in range(last_descriptor_i) :
    descriptor_and_label_string = descriptor_and_label_strings[i];
    descriptor_and_label_split = descriptor_and_label_string.split('\t\t');
    descriptor_string = descriptor_and_label_split[1];
    label_string = descriptor_and_label_split[0];
    print("Processing descriptor " + str(i + 1) + "/" + str(last_descriptor_i) + ": " + descriptor_string);
    # search for all matches to descriptor, and also grab surrounding words
    all_found = re.findall( regex % \
            re.escape(descriptor_string), filedata);
    descriptor = Descriptor(descriptor_string, label_string);
    if len(all_found) == 0:
        print("\tNO MATCH FOUND");

    for found in all_found:
        # pass the words on the the descriptor for it to add them to its
        # dictionary
        descriptor.add_words(found);

    descriptors.append(descriptor);

# string containing data to be written to file
file_data = '';

# set vectors for descriptors and set string to write data to file
for descriptor in descriptors:
    file_data += descriptor.get_title() + '\t' + descriptor.get_label() + '\t';
    for entry in descriptor.get_vector():
        file_data += str(entry) + ' ';
    file_data = file_data[0:-1];
    file_data += '\n';

with open(TRAINING_DATA_SELF_FILE, 'w') as file:
  file.write(file_data);
