# File: self_training_set_constructor.py 
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen
# Created: 31/01/2018
import re;
import random;

from constants import *;

sentence_regex = r'[^.\?\!]*[^A-Za-z]%s(?:[^A-Za-z\.\?\!][^.\?\!]*)?[\.\?\!]';
descriptor_regex = r'[^A-Za-z]%s[^A-Za-z\.\?\!]';

# get all descriptors and their labels as tab-separated in individual strings
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

# to hold all instance objects
instances = [];

# load the raw data
filedata = None;
with open(RAW_TEXT_FILE, 'r') as file :
  filedata = file.read();

last_descriptor_i = int(len(descriptor_and_label_strings) * VECTORIZED_PROP);

for i in range(last_descriptor_i) :
    descriptor_and_label_string = descriptor_and_label_strings[i];
    descriptor_and_label_split = descriptor_and_label_string.split('\t\t');
    descriptor_string = descriptor_and_label_split[1];
    label_string = descriptor_and_label_split[0];
    print("Processing descriptor " + str(i + 1) + "/" + str(last_descriptor_i) + ": " + descriptor_string);
    # search for all matches to descriptor, and also grab surrounding words in
    # the sentence TODO may not always grab entire sentence, e.g. "Mr. Mime" or
    # "A.J." somewhere in the sentence will throw it off
    all_found = re.findall( sentence_regex % re.escape(descriptor_string), 
        filedata);
    if len(all_found) == 0:
        print("\tNO MATCH FOUND");

    for found in all_found:
        # print('SENTENCE: ' + found);
        r = re.compile(descriptor_regex % descriptor_string);
        iterator = r.finditer(found)
        for match in iterator:
            descriptor_pos = match.span()[0] + 1;
            # print('\tMatch at: ' + str(descriptor_pos))
            instances.append(Instance(descriptor_string, descriptor_pos, found, 
                label_string));

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

# randomly shuffle strings
random.shuffle(data_lines_to_write);

# string containing data to be written to file
file_data = '';
file_data += str(len(instances[0].get_vector())) + '\n';

# set string to write data to file
for line in data_lines_to_write:
    file_data += line;

with open(TRAINING_DATA_SELF_FILE, 'w') as file:
  file.write(file_data);
