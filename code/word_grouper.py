# File: word_grouper.py 
# Author(s): Rishikesh Vaishnav, TODO
# Created: 27/02/2018
from sklearn.cluster import KMeans;
import numpy as np;
import random;
from constants import *;

# load the raw data
filedata = None;
with open(RAW_TEXT_FILE, 'r') as file :
  filedata = file.read();

def get_verb_vectors(verb_pivots):
    verbs_to_vectors = {};
    for verb in verb_pivots:
        print("verb: " + verb);
        instance_vectors = [];
        # TODO get vectors
        for conj in verb_pivots[verb]:
            print("\tconj: " + conj);
            conj_ins_ld = TSDescriptor(conj, None, filedata, True);
            conj_ins_ld.set_instances();
            for instance in conj_ins_ld.get_instances():
                instance_vectors.append(instance.get_vector());

        # --- average vectors ---

        instance_mx = np.zeros((len(instance_vectors), \
                len(instance_vectors[0])))

        for i in range(len(instance_vectors)):
            instance_mx[i, :] = instance_vectors[i];
        
        average_instance_vector_mx = np.mean(instance_mx, axis=0);

        average_instance_vector = average_instance_vector_mx.tolist();

        # ---

        # set the vector for this verb
        verbs_to_vectors[verb] = average_instance_vector;

    return verbs_to_vectors;

NUM_GROUPS = 3;

verb_pivots = json.load(open('pivot_conjs'));

#TODO remove
verb_pivots = {"say": ["saying", "say", "said", "says"], "copy": ["copied", "copy", "copies", "copying"], "yellow": ["yellowing", "yellowed", "yellows", "yellow"], "hitch": ["hitched", "hitches", "hitching", "hitch"], "protest": ["protesting", "protest", "protested", "protests"], "sleep": ["slept", "sleep", "sleeps", "sleeping"]};

verb_to_vectors = get_verb_vectors(verb_pivots);

rand_key = random.choice(list(verb_to_vectors.keys()))
dims = len(verb_to_vectors[rand_key]);

# set up vector with expected size
verb_vectors = np.zeros((len(verb_to_vectors), dims));

i = 0;
for verb in verb_to_vectors:
    verb_vectors[i, :] = verb_to_vectors[verb];
    i += 1;

# TODO better clusterer?
kmeans = KMeans(n_clusters=NUM_GROUPS, random_state=0).fit(verb_vectors);

groups_to_verbs = {};
for i in range(NUM_GROUPS):
    groups_to_verbs[str(i)] = [];

for verb in verb_to_vectors:
    group = kmeans.predict(np.array([verb_to_vectors[verb]]))[0];
    groups_to_verbs[str(group)] += verb_pivots[verb];

with open(PIVOT_CONJ_FILE, 'w') as file:
    file.write(json.dumps(groups_to_verbs));
