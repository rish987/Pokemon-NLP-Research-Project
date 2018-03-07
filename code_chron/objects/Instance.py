# File: Instance.py
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen
# Created: 06/03/2018
import re

D = 0.9;

ACTOR = 1;
TARGET = -1;
DIRECTIONS = [ACTOR, TARGET];

class Instance():
    def __init__(self, instance_text, _label_to_nums, pivots_list):
        instance_text_split = instance_text.split('\t');

        # extract descriptor, label, position, and sentence
        self.descriptor = instance_text_split[0];
        self.label = instance_text_split[1];
        self.descriptor_pos = int(instance_text_split[2]);
        sentence_text = instance_text_split[3];
        self.label_to_nums = _label_to_nums;
        sentence_text = re.sub(r'[^\w\s\'-]',' ',sentence_text).lower();
        sentence_text = sentence_text.replace('\n', '');
        self.context = sentence_text;
        
        self.vector = [];
        self.vector_dict = {};
        for pivots in pivots_list:
            self.process_pivots(pivots);

    def get_label(self):
        return self.label;

    def get_descriptor(self):
        return self.descriptor;

    def get_vector_dict(self):
        return self.vector_dict;

    def get_descriptor_pos(self):
        return self.descriptor_pos;

    def get_context(self):
        return self.context;

    def write_vector_to_file(self, filename):
        self.get_vector();

        with open(filename, 'a') as file:
          file.write(str(self.vector) + '\n');

    def get_vector(self):
        # sort alphabetically
        temp = [v for k, v in sorted(self.vector_dict.items())];

        vectorized = [];
        for entry in temp:
            vectorized += [v for k, v in sorted(entry.items())];

        vectorized.append(self.label_to_nums[self.label]);

        self.vector = vectorized;

    """
    Sets this instance's vector by searching for words in the context and
    identifying them as acting or targeting words.
    E.g., if the instance is "Bulbasaur" in the sentence "Bulbasaur uses Vine
    Whip.", "uses" is an acting pivot. On the other hand, if the instance is 
    "Vine Whip" in the sentence "Bulbasaur uses Vine Whip", "uses" is a
    targeting pivot.
    """
    def process_pivots(self, pivots):
        for pivot in pivots:
            if pivot not in self.vector_dict:
                # there are two entries per pivot; one set if this pivot is
                # used as an action this descriptor performs in this context
                # (ACTOR), and another set if this action is performed on this
                # descriptor in this context (TARGET)
                self.vector_dict[pivot] = {ACTOR: 0, TARGET: 0};
            
        text_dirs = {};

        text_dirs[ACTOR] = self.context[self.descriptor_pos \
                + len(self.descriptor):].split(' ');
        text_dirs[ACTOR] = [x for x in text_dirs[ACTOR] if x];

        text_dirs[TARGET] = self.context[0:self.descriptor_pos].split(' ');
        text_dirs[TARGET] = [x for x in text_dirs[TARGET] if x];

        conjs = [];
        for pivot in pivots:
            conjs += pivots[pivot];

        # go left and right
        for direction in DIRECTIONS:
            words = text_dirs[direction];

            # current word index
            c_i = 0;

            # number of pivots found
            num_found = 0;

            # distance from current word
            d_i = 0;

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
                    found = [k for k,v in pivots.items() if word in v][0];

                    # weighted value for distance
                    d_weighted = D * (float(1) / float(d_i + 1));

                    # weighed value for number found
                    n_weighted = (1 - D) * \
                        (float(1) / float(num_found + 1));

                    direction_to_set = direction;

                    self.vector_dict[found][direction_to_set] = d_weighted \
                        + n_weighted;

                    num_found += 1;

                # go to next word
                c_i += direction;

                d_i += 1;
