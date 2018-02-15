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
TODO active vs passive voice
TODO multiple instances in one sentence
"""
ACTOR = 1;
TARGET = -1;

text = 'Ash used Bulbasaur next and it swiftly used its Vine Whip attack.';
instance_texts = ['Ash', 'Bulbasaur', 'Vine Whip'];
verbs = {'use': ['used']};

TEMPLATE_VECTOR = {};

directions = [ACTOR, TARGET];

for verb in verbs:
    # there are two entries per verb; one set if this verb is used as an action
    # this descriptor performs in this context (ACTOR), and another set if this
    # action is performed on this descriptor in this context (TARGET)
    TEMPLATE_VECTOR[verb] = {ACTOR: 0, TARGET: 0};

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
    Whip.", "uses" is an acting verb. On the other hand, if the instance is 
    "Vine Whip" in the sentence "Bublasaur uses Vine Whip", "uses" is a
    targeting verb.
    """
    def set_vector(self):
        # set template vector of this instance to fill
        self.vector = copy.deepcopy(TEMPLATE_VECTOR);

        # get index 
        self.descriptor_pos = self.descriptor_pos;

        text_dirs = {};

        text_dirs[ACTOR] = self.context[self.descriptor_pos + len(self.descriptor):];
        text_dirs[TARGET] = self.context[0:self.descriptor_pos];

        # go through all verbs
        for verb in verbs:
            # conjugations
            conjs = verbs[verb];

            # go left and right
            for direction in directions:
                text_dir = text_dirs[direction];

                # split up self.context by word
                words = text_dir.split(' ');

                # current word index
                c_i = 0;

                # going backward; start at last word
                if direction == TARGET:
                    c_i = len(words) - 1;
                # going foward; start at first word
                elif direction == ACTOR:
                    c_i = 0;

                # stop after leaving the sentence
                while (c_i >= 0) and (c_i <= (len(words) - 1)):
                    # extract this word
                    word = words[c_i];

                    # this word is a conjugation of the verb
                    if word in conjs:
                        # set value of actor/target in vector corresponding to
                        # verb in this specific instance
                        self.vector[verb][direction] = 1;

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
