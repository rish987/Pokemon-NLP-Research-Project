import pickle ;
from constants import * ;

sentences = [] ;

with open(RELATION_SENTENCES_FILE, 'rb') as file:
    sentences = pickle.load(file);

print(sentences) ;
