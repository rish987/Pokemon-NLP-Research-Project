# File: global_pivots_constructor.py 
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen
# Created: 08/04/2018
from constants import *;
import pickle;
import re;

# matches the current descriptor and a following word
DESCRIPTOR_AND_NEXT_WORD_REGEX = r'%s %s';

# matches the current descriptor alone
DESCRIPTOR_REGEX = r'\b%s\b';

# file containing text from all episodes
ALL_EPISODE_TEXT_FILE = "../data/data";

all_episode_text = '';

with open(ALL_EPISODE_TEXT_FILE, 'r') as file:
    all_episode_text = file.read();

# to hold mapping from descriptor to global pivot category to boolean
descriptors_to_global_pivots = {};

# to hold mapping of descriptors to labels
descriptors_to_labels = {};

# open file and save lines to array
descriptors_labeled_file_lines = [];
with open(DESCRIPTORS_LABELED_FILE, 'r') as file:
    descriptors_labeled_file_lines = file.read().splitlines();


# construct dictionary mapping
for line in descriptors_labeled_file_lines:
    split = line.split('\t');
    label = split[0];
    descriptor = split[1];
    descriptors_to_labels[descriptor] = label;

descriptors = descriptors_to_labels.keys();

# --- initialize mapping ---

for descriptor in descriptors:
    for word in descriptor.split():
        descriptors_to_global_pivots[word] = {};

    for pivot_category in global_pivots:
        for word in descriptor.split():
            descriptors_to_global_pivots[word][pivot_category] = False;

# --- 

num_descriptors = len(descriptors);
descriptor_i = 0;

false_pos_count = 0;
false_neg_count = 0;

for descriptor in descriptors:
    print("Processing descriptor " + descriptor + ": " +\
        str(descriptor_i + 1) + "/" + str(num_descriptors));
    label = descriptors_to_labels[descriptor];
    num_descriptor_matches = len(re.findall(DESCRIPTOR_REGEX % descriptor,\
        all_episode_text));

    for pivot_category in global_pivots:
        num_pivot_matches = 0;

        num_pivots = len(pivots);
        pivot_i = 0;

        found_any_bool = False;

        for pivot in global_pivots[pivot_category] :
            #print("\tProcessing pivot " + pivot + ": " + str(pivot_i + 1) +\
            #        "/" + str(num_pivots));
            found = re.findall(DESCRIPTOR_AND_NEXT_WORD_REGEX % \
                    (descriptor, pivot), all_episode_text);

            num_pivot_matches += len(found);

            found_bool = len(found) > 0;

            if found_bool:
                found_any_bool = True;

                for word in descriptor.split():
                    descriptors_to_global_pivots[word][pivot_category] \
                        = True;
                    #print("found");


            pivot_i += 1;

        pivot_proportion = float(num_pivot_matches) / \
            float(num_descriptor_matches);

        # false positive
        if found_any_bool:
            print("Proportion of occurrences with pivots: " + str(pivot_proportion));
            if (label != 'person'):
                print("FALSE POSITIVE");
                false_pos_count += 1;

        # false negative
        if (not found_any_bool) and (label == 'person'):
            #print("FALSE NEGATIVE");
            false_neg_count += 1;


    descriptor_i += 1;

print("False positives: " + str(false_pos_count))
print("False negatives: " + str(false_neg_count))

with open(DESCRIPTORS_TO_GLOBAL_PIVOTS_FILE, 'wb') as file:
    pickle.dump(descriptors_to_global_pivots, file);
