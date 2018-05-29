# File: grapher.py 
# Author(s): Rishikesh Vaishnav, TODO
# Created: 21/02/2018

import numpy as np;
import matplotlib.pyplot as mpl;

data = np.loadtxt('graph_data_s');

sizes = data[:, 0];
acc_inst = data[:, 1];
acc_desc = data[:, 2];
acc_dumm = data[:, 3];

mpl.plot(sizes, acc_inst, label='Instance Accuracy');
mpl.plot(sizes, acc_desc, label='Descriptor Accuracy');
mpl.plot(sizes, acc_dumm, label='Dummy (Stratified Random) Accuracy');
mpl.xlabel('Training Data Size');
mpl.ylabel('Accuracy');
mpl.title('Training Set Size and Classifier Accuracies');
mpl.legend();
mpl.show();
