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
TODO incorrectly matching pronouns to actor/target (e.g. "Ash brushes its
    fur.")
TODO 'Team Rocket Grunt' no match found?
TODO multiple pivots
    TODO multiple pivots in a row get similar weights, i.e. 'was used'
TODO not detecting pivots when it should?
"""
ACTOR = 1;
TARGET = -1;

text = 'Ash used Bulbasaur next and it swiftly used its Vine Whip attack';
"""
Active/Passive voice Probability Heuristic

text = '* * * Vine Whip was used by Bulbasaur';

IDEAL
Vine Whip - 'used': {ACTOR: 0, TARGET: 1}
Bulbasaur - 'used': {ACTOR: 1, TARGET: 0}

WITHOUT CHECKING
Vine Whip - 'used': {ACTOR: 1, TARGET: 0}
Bulbasaur - 'used': {ACTOR: 0, TARGET: 1}

???
passive_voice_prob = (1/[dist. to 'was'] + 1/[dist. to 'by']) / [total number of words]

"""
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
        self.vector = {};
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

        conjs = [];
        for pivot in pivots:
            conjs += pivots[pivot];

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
                    # use the key as the found pivot in this direction
                    found = [k for k,v in pivots.items() if word in\
                            v][0];

                    self.vector[found][direction] = 1;

                    # TODO may want to consider subsequent matches
                    break;

                # go to next word
                c_i += direction;

# go through all instances of descriptors
for instance_text in instance_texts:
    # create a new instance
    instance = Instance(instance_text, text.index(instance_text), text);
    instances.append(instance);

    print("Instance: " + instance.get_descriptor());
    print("\t" + str(instance.get_vector_dict()));
