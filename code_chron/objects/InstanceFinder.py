# File: InstanceFinder.py
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen
# Created: 06/03/2018
import re;

SENTENCE_REGEX = r'[^.\?\!]*[^A-Za-z]%s(?:[^A-Za-z\.\?\!][^.\?\!]*)?[\.\?\!]';
DESCRIPTOR_REGEX = r'[^A-Za-z]%s[^A-Za-z]';

class InstanceFinder():
    def __init__(self, _descriptor, _label, _text, _instances_filename):
        self.descriptor = _descriptor; 
        self.label = _label; 
        self.text = _text;
        self.instances_filename = _instances_filename;
        self.instances = [];

    def find_instances(self):
        # search for all matches to descriptor, and also grab surrounding words
        # in the sentence 
        # TODO may not always grab entire sentence, e.g. "Mr.  Mime" or "A.J."
        # somewhere in the sentence will throw it off
        all_found = re.findall(SENTENCE_REGEX % re.escape(self.descriptor), 
            self.text);

        if len(all_found) == 0:
            print("\tNO MATCH FOUND");

        # go through all sentences containing this desriptor
        for found in all_found:
            # find all matches for this descriptor in this sentence
            r = re.compile(DESCRIPTOR_REGEX % re.escape(self.descriptor));
            iterator = r.finditer(found)
            for match in iterator:
                descriptor_pos = match.span()[0] + 1;
                instance_line = '';
                instance_line += self.descriptor + '\t';
                instance_line += self.label + '\t';
                instance_line += str(descriptor_pos) + '\t';
                instance_line += found + '\t';

                # add a new instance for this instance
                self.instances.append(instance_line);

    def write_instances(self):
        to_write = '';
        for instance_line in self.instances:
            to_write += instance_line + '\n';

        with open(self.instances_filename, 'a') as file:
          file.write(to_write);
