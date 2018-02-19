# File: instance_loader.py 
# Author(s): Rishikesh Vaishnav, TODO
# Created: 19/02/2018

from constants import *;

# load the raw data
filedata = None;
with open(RAW_TEXT_FILE, 'r') as file :
  filedata = file.read();

# get all descriptors and their labels as tab-separated in individual strings
descriptor_and_label_strings = [];
with open(LABELED_CORRECTED_DESCRIPTORS_FILE) as f:
    descriptor_and_label_strings = f.read().splitlines();

# to hold list of all descriptor objects
ts_descriptors = [];

instances = [];

for i in range(len(descriptor_and_label_strings)):
    print(str(i + 1) + '/' + str(len(descriptor_and_label_strings)));
    descriptor_and_label_string = descriptor_and_label_strings[i];
    descriptor_and_label_split = descriptor_and_label_string.split('\t\t');
    descriptor_string = descriptor_and_label_split[1];
    label_string = descriptor_and_label_split[0];
    # create a new TSDescriptor for this descriptor
    ts_descriptor = TSDescriptor(descriptor_string, label_string, filedata);

    ts_descriptor.set_instances();

    instances += ts_descriptor.get_instances();

instance_filedata = '';
for instance in instances:
    instance_filedata += instance.get_descriptor() + '\t';
    instance_filedata += instance.get_label() + '\t';
    instance_filedata += str(instance.get_descriptor_pos()) + '\t';
    instance_filedata += instance.get_context() + '\t';
    instance_filedata += '\n';

with open(INSTANCE_FILE, 'w') as file:
  file.write(instance_filedata);
