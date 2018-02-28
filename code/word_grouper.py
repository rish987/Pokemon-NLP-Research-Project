# File: word_grouper.py 
# Author(s): Rishikesh Vaishnav, TODO
# Created: 27/02/2018
from sklearn.cluster import KMeans;
import numpy as np;
import random;
from constants import *;

# load the instance data
lines = None;
with open(VERB_INSTANCES_FILE, 'r') as file :
  lines = file.read().splitlines();

DELIMETER = '\t';

def get_verb_vectors(verb_pivots):
    verbs_to_vectors = {};
    total_verbs = len(verb_pivots);
    num_processed = 0;
    for verb in verb_pivots:
        print("verb " + str(num_processed + 1) + "/" + str(total_verbs) + ": " + verb);
        instance_vectors = [];
        # TODO get vectors
        for conj in verb_pivots[verb]:
            print("\tconj: " + conj);
            matching_lines = [l for l in lines if l.startswith(conj +\
                DELIMETER)];
            for line in matching_lines:
                line_split = line.split('\t');

                # extract descriptor, label, position, and sentence
                descriptor_string = line_split[0];
                label_string = line_split[1];
                pos = int(line_split[2]);
                sentence_string = line_split[3];

                # create a new instance for this, and add to list of instances
                instance = Instance(descriptor_string, pos, sentence_string, \
                    label_string, 0.9, True);
                instance_vectors.append(instance.get_vector());

        if len(instance_vectors) > 0:
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
        
        num_processed += 1;

    return verbs_to_vectors;

NUM_GROUPS = 200;

verb_pivots = json.load(open('pivot_conjs'));

verb_to_vectors = get_verb_vectors(verb_pivots);

rand_key = random.choice(list(verb_to_vectors.keys()))
dims = len(verb_to_vectors[rand_key]);

# set up vector with expected size
verb_vectors = np.zeros((len(verb_to_vectors), dims));

i = 0;
for verb in verb_to_vectors:
    verb_vectors[i, :] = verb_to_vectors[verb];
    i += 1;

for i in range(1, 11):
    num_groups = i * 100;
    print('num_groups: ' + str(num_groups));
    # TODO better clusterer?
    kmeans = KMeans(n_clusters=num_groups, random_state=0, \
        verbose=1).fit(verb_vectors);

    groups_to_verbs = {};
    for i in range(num_groups):
        groups_to_verbs[str(i)] = [];

    for verb in verb_to_vectors:
        group = kmeans.predict(np.array([verb_to_vectors[verb]]))[0];
        groups_to_verbs[str(group)] += verb_pivots[verb];

    with open(PIVOT_CONJ_FILE + '_' + str(num_groups), 'w') as file:
        file.write(json.dumps(groups_to_verbs));
