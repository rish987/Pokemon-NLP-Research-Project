# File: word_grouper_loader.py 
# Author(s): Rishikesh Vaishnav, TODO
# Created: 27/02/2018
from constants import *;

# clear the file
with open(VERB_INSTANCES_FILE, 'w') as file :
    file.close();
    
# load the raw data
filedata = None;
with open(RAW_TEXT_FILE, 'r') as file :
  filedata = file.read();


def write_verb_instances(verb_pivots):
    total_verbs = len(verb_pivots);
    num_processed = 0;
    for verb in verb_pivots:
        print("verb " + str(num_processed + 1) + "/" + str(total_verbs) + ": " + verb);
        # TODO get vectors
        for conj in verb_pivots[verb]:
            print("\tconj: " + conj);
            conj_ins_ld = TSDescriptor(conj, "none", filedata, True);
            conj_ins_ld.set_instances();
            for instance in conj_ins_ld.get_instances():
                instance.write_to_file(VERB_INSTANCES_FILE);

        num_processed += 1;

verb_pivots = json.load(open('pivot_conjs'));

write_verb_instances(verb_pivots);
