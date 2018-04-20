# File: openie_runner.py 
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen
# Created: 19/04/2018
# Description:
# Runs OpenIE separately for each episode, appending each result to a file.
import subprocess;
from constants import *;

# clear the file
with open(OPENIE_OUTPUT_FILE, 'w') as file:
    file.close();

# go through all episodes
for ep_num in range(1, NUM_EPS + 1):
    print('Processing episode: ' + str(ep_num) + '/' + \
        str(NUM_EPS));
    cmd = 'cd ~/Programming/stanford-corenlp-full-2018-02-27; \
    java -mx4g -cp "*" edu.stanford.nlp.naturalli.OpenIE \
    ~/Research/pokemon_nlp/code_relation_extraction/data/text/' + \
    EP_NUMBER_FORMAT % ep_num + \
    ' >> ~/Research/pokemon_nlp/code_relation_extraction/';

    # TODO set this_openie_out
    subprocess.Popen(cmd);
