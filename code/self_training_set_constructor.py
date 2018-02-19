# File: self_training_set_constructor.py 
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen
# Created: 31/01/2018
import re;
import random;

from constants import *;

sentence_regex = r'[^.\?\!]*[^A-Za-z]%s(?:[^A-Za-z\.\?\!][^.\?\!]*)?[\.\?\!]';
descriptor_regex = r'[^A-Za-z]%s[^A-Za-z]';

# load the raw data
filedata = None;
with open(RAW_TEXT_FILE, 'r') as file :
  filedata = file.read();

class TSDescriptor():
    def __init__(self, _descriptor, _label):
        self.descriptor = _descriptor;
        self.label = _label;
        self.instances = [];
        self.instance_ind = -1;
        self.got_instances = False;

    def get_instances(self):
        # search for all matches to descriptor, and also grab surrounding words
        # in the sentence TODO may not always grab entire sentence, e.g. "Mr.
        # Mime" or "A.J." somewhere in the sentence will throw it off
        all_found = re.findall( sentence_regex % re.escape(self.descriptor), 
            filedata);
        if len(all_found) == 0:
            print("\tNO MATCH FOUND");

        for found in all_found:
            # print('SENTENCE: ' + found);
            r = re.compile(descriptor_regex % self.descriptor);
            iterator = r.finditer(found)
            for match in iterator:
                descriptor_pos = match.span()[0] + 1;
                # print('\tMatch at: ' + str(descriptor_pos))
                self.instances.append(Instance(self.descriptor, \
                    descriptor_pos, found, self.label));

        self.got_instances = True;

    def rem_instances(self):
        return (not self.got_instances) or ((self.instance_ind + 1) \
            < len(self.instances));

    def get_next_instance(self):
        if not self.got_instances:
            self.get_instances();
        # TODO bound check
        if (self.instance_ind + 1) >= len(self.instances):
            return None;
        self.instance_ind += 1;
        return self.instances[self.instance_ind];

# get all descriptors and their labels as tab-separated in individual strings
descriptor_and_label_strings = [];
with open(LABELED_CORRECTED_DESCRIPTORS_FILE) as f:
    descriptor_and_label_strings = f.read().splitlines();

# to hold mapping from labels to all descriptor objects of those labels
ts_descriptors = {};
for label in label_nums:
    ts_descriptors[label] = [];

for i in range(len(descriptor_and_label_strings)):
    descriptor_and_label_string = descriptor_and_label_strings[i];
    descriptor_and_label_split = descriptor_and_label_string.split('\t\t');
    descriptor_string = descriptor_and_label_split[1];
    label_string = descriptor_and_label_split[0];
    # create a new TSDescriptor for this descriptor
    ts_descriptor = TSDescriptor(descriptor_string, label_string);

    ts_descriptors[label_string].append(ts_descriptor);

instances = [];

for i in range(TRAINING_SET_SIZE_PER_LABEL):
    print("Processing instance: " + str(i + 1) + "/" \
        + str(TRAINING_SET_SIZE_PER_LABEL));
    l_i = 0;
    for label in label_nums:
        print("\tProcessing label: " + str(l_i + 1) + "/" \
            + str(len(label_nums)));
        des_list = ts_descriptors[label];
        random.shuffle(des_list);
        num_ts_descriptors = len(des_list);

        instance = None;
        for i in range(num_ts_descriptors):
            if des_list[i].rem_instances():
                instance = des_list[i].get_next_instance();
                break;

        if instance == None:
            print("[WARNING] No remaining instances for label: " + label);
        else:
            instances.append(instance);

        l_i += 1;

#TODO create instances

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
