# File: blocked_training_set_constructor.py 
# Author(s): Rishikesh Vaishnav, TODO
# Created: 19/02/2018

from constants import *;

NUM_BLOCKS = 5;

with open(TRAINING_DATA_SELF_FILE, 'w') as file:
  file.close();

# get all descriptors and their labels as tab-separated in individual strings
instance_strings = [];
with open(INSTANCE_FILE) as f:
    instance_strings = f.read().splitlines();

num_per_block = len(instance_strings) / NUM_BLOCKS;

for i in range(NUM_BLOCKS):
    construct_training_set(i * num_per_block, num_per_block);

def construct_training_set(start_ind, block_size):

