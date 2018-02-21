# File: experimenter.py 
# Author(s): Rishikesh Vaishnav, TODO
# Created: 20/02/2018
from classifier import *;
from self_training_set_constructor import *;

GRAPH_FILE = 'graph_data';

# number of classification trials to average over
NUM_TRIALS = 5;

instance_data = get_labels_to_instances();
instance_strings = instance_data['instance_strings'];
labels_to_instances = instance_data['labels_to_instances'];

s_vals = [];
inst_acc_vals = [];
desc_acc_vals = [];
dummy_acc_vals = [];
for i in range(0, 1):
    print("Iteration: " + str(i));
    d = 0.9; # TODO
    s = 150; 
    s_vals.append(s * len(label_nums) * TRAINING_SET_PROP);
    self_training_set_constructor(instance_strings, labels_to_instances, d, s);

    sum_inst_classify = 0;
    sum_desc_classify = 0;
    sum_dummy_classify = 0;

    data_info = get_data_info();
    data = data_info['data'];
    descriptors = data_info['descriptors'];
    descriptors_to_labels = data_info['descriptors_to_labels'];

    for j in range(NUM_TRIALS):
        print
        results = classify(data, descriptors, descriptors_to_labels, False,\
                True);

        sum_inst_classify += results['log_reg'];
        sum_desc_classify += results['desc_classify'];
        sum_dummy_classify += results['dummy'];

        print("Trials complete: " + str(j + 1) + "/" + str(NUM_TRIALS));

    print("Average instance classification result over " + str(NUM_TRIALS) + \
            " trials: ");
    inst_acc_val = float(sum_inst_classify) / float(NUM_TRIALS);
    inst_acc_vals.append(inst_acc_val)
    print(str(inst_acc_val));

    print("Average descriptor classification result over " + str(NUM_TRIALS) + \
            " trials: ");
    desc_acc_val = float(sum_desc_classify) / float(NUM_TRIALS);
    desc_acc_vals.append(desc_acc_val)
    print(str(desc_acc_val));

    print("Average dummy result over " + str(NUM_TRIALS) + \
            " trials: ");
    dummy_acc_val = float(sum_dummy_classify) / float(NUM_TRIALS);
    dummy_acc_vals.append(dummy_acc_val)
    print(str(dummy_acc_val));

lines_to_write = [];

for i in range(len(s_vals)):
    line = str(s_vals[i]) + ' ' + \
            str(inst_acc_vals[i]) + ' ' + \
            str(desc_acc_vals[i]) + ' ' + \
            str(dummy_acc_vals[i]) + ' ' + \
            '\n';
    lines_to_write.append(line);

file_data = '';

for line in lines_to_write:
    file_data += line;

with open(GRAPH_FILE, 'w') as file:
  file.write(file_data);
