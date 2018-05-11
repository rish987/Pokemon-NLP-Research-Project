# Filename: generate_vector
# Description: Takes a triple generated by OpenIE as argument and outputs a
#              vector representation of that triple. The first 10 features will
#              indicate the label of the subject, the last 10 features will
#              indicate the label of the object, and the remaining features in
#              the middle will be generated based on word2vec.

from constants import * ;
import numpy as np ;
import re;
import gensim;
# to hold mapping of descriptors to labels and descriptors ordered by length
descriptors_to_labels, descriptors_ordered = get_dictionary_desc_to_labels() ;
VECTOR_SIZE = 100;

all_text = ''
with open(ALL_TEXT_FILE, 'r') as file:
    all_text = str(file.read());
all_text = all_text.replace('\n', '');
all_text_sentences = all_text.split('.');

# remove empty sentences
all_text_sentences = [ sentence.split() for sentence in \
    all_text_sentences if len(sentence) > 0];

model = gensim.models.Word2Vec(all_text_sentences, size=VECTOR_SIZE, \
        window=5, min_count=5, workers=4)

# finds the descriptor (if one exists) in the phrase and returns its label
def assign_label (desc_phrase):
    # iterate through ordered descriptors
    for descriptor in descriptors_ordered:
        r = re.search(r'\b%s\b' % re.escape(descriptor), desc_phrase);
        # if a descriptor is found, index into dictionary to return its label
        if r != None:
            return descriptors_to_labels[descriptor] ;

    # no descriptor was found in the phrase
    return None ;

# returns a list/vector of 10 binary features corresponding to the given label
def create_label_vector (label):
    label_vector = [(1 if (label == x) else 0) for x in \
        descriptor_labels_alpha] ;

    return np.array(label_vector) ;
    # for label_type in descriptor_labels_alpha:

# returns the normalized sum of the word vectors generated by word2vec for each
# word in the segment
# TODO
def vectorize_action (action):
    action_words = action.split(' ');

    # initialize zero-filled sum array
    vector_sum = np.zeros((VECTOR_SIZE,));

    for word in action_words:
        if word in model.wv: 
            vector_sum += model.wv[word];

    return vector_sum;

def generate_triple_vector (triple):
    # parse the triple into its constituents
    triple_segments = triple.split('\t') ;

    subj = triple_segments[1] ;
    action = triple_segments[2] ;
    obj = triple_segments[3] ;

    # label the subject and object from the triple
    subj_label = assign_label(subj) ;
    obj_label = assign_label(obj) ;

    # turn those labels into 10-feature vectors
    subj_vector = create_label_vector(subj_label) ;
    obj_vector = create_label_vector(obj_label) ;

    # process the action segment of the triple with word2vec or similar
    action_vector = vectorize_action(action) ;

    # concatenate vectors together to produce output
    output_vector = np.concatenate((subj_vector, action_vector, \
        obj_vector), axis=0) ;

    return output_vector ;

#create_label_vector(assign_label("Ash sends out Bulbasaur"));
print(generate_triple_vector("1.0\tAsh\tsends out\tBulbasaur"));

vectorize_action('use');
