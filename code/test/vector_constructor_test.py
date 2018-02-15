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

text = 'Ash used Bulbasaur next and it swiftly used its Vine Whip attack.';
instances = ['Ash', 'Bulbasaur', 'Vine Whip'];
verbs = {'use': ['used']};

ACTOR = 1;
TARGET = -1;

TEMPLATE_VECTOR = {};

vectors = {};

directions = [ACTOR, TARGET];

for verb in verbs:
    TEMPLATE_VECTOR[verb] = {ACTOR: 0, TARGET: 0};

# go through all instances of descriptors
for instance in instances:
    print('instance: ' + instance);

    # set template vector of this instance to fill
    vectors[instance] = copy.deepcopy(TEMPLATE_VECTOR);
    print(vectors[instance]);

    # get index TODO should get index from instance  TODO should get text from
    # instance
    d_i = text.index(instance);

    text_dirs = {};

    text_dirs[ACTOR] = text[d_i + len(instance):];
    text_dirs[TARGET] = text[0:d_i];

    # go through all verbs
    for verb in verbs:
        print('\tverb: ' + verb);
        # conjugations
        conjs = verbs[verb];

        # go left and right
        for direction in directions:
            print('\t\tdir: ' + str(direction));
            text_dir = text_dirs[direction];
            print('\t\t' + text_dir);

            # split up text by word
            words = text_dir.split(' ');

            # current word index
            c_i = 0;

            # going foward
            if direction == TARGET:
                c_i = len(words) - 1;
            elif direction == ACTOR:
                c_i = 0;

            # stop after leaving the sentence
            while (c_i >= 0) and (c_i <= (len(words) - 1)):
                # extract this word
                word = words[c_i];
                print('\t\t\t' + word);

                # this word is a conjugation of the verb
                if word in conjs:
                    # set value of actor/target in vector corresponding to verb
                    # in this specific instance
                    print('here')
                    vectors[instance][verb][direction] = 1;

                    # TODO may want to consider subsequent matches
                    break;

                # go to next word
                c_i += direction;

print(vectors);
