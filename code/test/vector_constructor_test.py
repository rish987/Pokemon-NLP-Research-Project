# File: [FILENAME] 
# Author(s): Rishikesh Vaishnav, TODO
# Created: 15/02/2018
import copy;

"""
IDEAL
Ash:
[ used_act: 1, used_tar: 0 ]
Bulbasaur:
[ used_act: 1, used_tar: 1 ]
Vine Whip:
[ used_act: 0, used_tar: 1 ]
"""

"""
TODO part of speech tagging: only pivot on a certain part of speech to
     improve performance (e.g. not pivoting on "attack" in the following
     example, as it is not a verb)
     ex: 'Ash used Bulbasaur next and it swiftly used its Vine Whip attack.'
TODO multiple pivots for a single entity, e.g.
     [Ash] congratulates [Caterpie] on coming through, and urges [Misty]...
TODO confidence based on distance
TODO active vs passive voice
TODO filter out punctuation
"""
ACTOR = 1;
TARGET = -1;

text = 'Ash used Bulbasaur next and it swiftly used its Vine Whip attack';
instance_texts = ['Ash', 'Bulbasaur', 'Vine Whip'];
pivots = {'use': ['used'], 'attack': ['attack']};

TEMPLATE_VECTOR = {};

directions = [ACTOR, TARGET];

for pivot in pivots:
    # there are two entries per pivot; one set if this pivot is used as an
    # action this descriptor performs in this context (ACTOR), and another set
    # if this action is performed on this descriptor in this context (TARGET)
    TEMPLATE_VECTOR[pivot] = {ACTOR: 0, TARGET: 0};

instances = [];

class Instance():
    """
    Initialize this Instance with the given context (containing sentence),
    label, and construct this instance's vector.

    _descriptor - the descriptor that generated this instance
    _context - the sentence in which the descriptor was found
    _descriptor_pos - the index of the match to descriptor in the context; 0
    unless there are more than one matches
    """
    def __init__(self, _descriptor, _descriptor_pos, _context):
        self.descriptor = _descriptor;
        self.descriptor_pos = _descriptor_pos;
        self.context = _context;
        self.vector = [];
        self.set_vector();

    def get_descriptor(self):
        return self.descriptor;

    def get_vector_dict(self):
        return self.vector;

    """
    Sets this instance's vector by searching for words in the context and
    identifying them as acting or targeting words.
    E.g., if the instance is "Bulbasaur" in the sentence "Bublasaur uses Vine
    Whip.", "uses" is an acting pivot. On the other hand, if the instance is 
    "Vine Whip" in the sentence "Bulbasaur uses Vine Whip", "uses" is a
    targeting pivot.
    """
    def set_vector(self):
        # set template vector of this instance to fill
        self.vector = copy.deepcopy(TEMPLATE_VECTOR);

        text_dirs = {};

        text_dirs[ACTOR] = self.context[self.descriptor_pos \
                + len(self.descriptor):].split(' ');
        text_dirs[TARGET] = self.context[0:self.descriptor_pos].split(' ');

        # to store nearest pivot to this instance
        nearest_pivots_inds = {};
        # ACTOR means tracking running min
        nearest_pivots_inds[ACTOR] = len(text_dirs[ACTOR]) + 1;
        # TARGET means tracking running max
        nearest_pivots_inds[TARGET] = -1;

        # go through all pivots
        for pivot in pivots:
            # conjugations
            conjs = pivots[pivot];

            # go left and right
            for direction in directions:
                words = text_dirs[direction];

                # current word index
                c_i = 0;

                if direction == TARGET:
                    # going backward; start at last word
                    c_i = len(words) - 1;
                elif direction == ACTOR:
                    # going foward; start at first word
                    c_i = 0;

                # stop after leaving the sentence
                while (c_i >= 0) and (c_i <= (len(words) - 1)):
                    # extract this word
                    word = words[c_i];

                    # this word is a conjugation of the pivot
                    if word in conjs:
                        if direction == TARGET:
                            if c_i > nearest_pivots_inds[TARGET]:
                                nearest_pivots_inds[TARGET] = c_i;
                        elif direction == ACTOR:
                            if c_i < nearest_pivots_inds[ACTOR]:
                                nearest_pivots_inds[ACTOR] = c_i;

                        # TODO may want to consider subsequent matches
                        break;

                    # go to next word
                    c_i += direction;

        # a pivot was found
        if (nearest_pivots_inds[ACTOR] != len(text_dirs[ACTOR]) + 1):
            # set actor value in vector corresponding to nearest actor pivot 
            idx = nearest_pivots_inds[ACTOR];
            pivot = text_dirs[ACTOR][idx];

            # get the unconjugated form from the dictionary
            # TODO may be slow, consider bringing in parallel data structure
            pivot_unconj = [k for k,v in pivots.items() if pivot in v][0];
            
            self.vector[pivot_unconj][ACTOR] = 1;

        # a pivot was found
        if(nearest_pivots_inds[TARGET] != -1):
            # set target value in vector corresponding to nearest target pivot 
            idx = nearest_pivots_inds[TARGET];
            pivot = text_dirs[TARGET][idx];

            # get the unconjugated form from the dictionary
            pivot_unconj = [k for k,v in pivots.items() if pivot in v][0];
            
            self.vector[pivot_unconj][TARGET] = 1;

# go through all instances of descriptors
for instance_text in instance_texts:
    # create a new instance
    instance = Instance(instance_text, text.index(instance_text), text);
    instances.append(instance);

    print("Instance: " + instance.get_descriptor());
    print("\t" + str(instance.get_vector_dict()));
