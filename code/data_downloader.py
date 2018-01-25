# File: data_downloader.py 
# Author(s): Rishikesh Vaishnav, Jessica Lacovelli, Bonnie Chen
# Created: 23/01/2018

from urllib.request import Request, urlopen;
from html.parser import HTMLParser
import re
import enchant
import shutil

# expected tag and attributes of plot header
PLOT_TAG = 'span'
PLOT_ATTRS = [('class', 'mw-headline'), ('id', 'Plot')];

# tag used for hyperlink
LINK_TAG = 'a'

# total number of episodes in the first generation
NUM_EPS = 116;

# bulbapedia wiki URL prefix
URL_PREFIX = 'https://bulbapedia.bulbagarden.net/wiki/EP';

# regular expression to remove parentheses from a string
REMOVE_PARENS_REGEX = r'\([^)]*\)';

# files to write to
RAW_TEXT_FILE = '../data/data';
ANNOTATED_TEXT_FILE = '../data/data_annotated';

# files to write data to
raw_text_file = open(RAW_TEXT_FILE, 'w');

# dictionary of rigid descriptors and their labels
rigid_descriptors = {};

# special characters that could be part of a descriptor
SPECIAL_CHARACTERS = ['.'];

# class for processing HTML files
class MyHTMLParser(HTMLParser):
    # add instance variables
    def __init__(self):
        super(MyHTMLParser, self).__init__()
        self.parsing_plot = False;
        self.just_seen_plot_tag = False;
        self.in_hyperlink = False;
        self.current_hyperlink = "";

    def handle_starttag(self, tag, attrs):
        if self.parsing_plot:
            # this is a new header seen while parsing under the plot header, so
            # the plot description must be over
            if tag == PLOT_TAG:
                self.parsing_plot = False;

            elif tag == LINK_TAG:
                matching_attrs = [x for x in attrs if x[0] == 'title'];
                if len(matching_attrs) > 0:
                    # indicate that currently parsing hyperlink
                    self.in_hyperlink = True;
                    # set current hyperlink
                    self.current_hyperlink = re.sub(REMOVE_PARENS_REGEX, '', matching_attrs[0][1]);
        # not currently parsing the plot, but just encountered a plot header
        elif self.is_plot_header(tag, attrs):
            self.just_seen_plot_tag = True;

    """
    Determines whether the given tag and attributes indicate a plot section 
    header. 
    """
    def is_plot_header(self, tag, attrs):
        # this is not a header
        if tag != PLOT_TAG:
            return False;

        plot_attr = True;
        
        # go through all of the required attributes
        for attr in PLOT_ATTRS:
            # this attribute was not found in the actual list of attributes, so
            # this cannot be a plot header
            if attr not in attrs:
                plot_attr = False;

        return plot_attr;

    def handle_endtag(self, tag):
        # closing plot header span
        if self.just_seen_plot_tag and (tag == PLOT_TAG):
            # indicate that now parsing plot
            self.parsing_plot = True;
            self.just_seen_plot_tag = False;
        elif self.parsing_plot:
            # closing a hyperlink
            if tag == LINK_TAG and self.in_hyperlink:
                self.in_hyperlink = False;

    def handle_data(self, data):
        if self.parsing_plot:
            raw_text_file.write(data);

            # need to add this data to the dictionary
            if self.in_hyperlink:
                if self.current_hyperlink not in rigid_descriptors:
                    rigid_descriptors[self.current_hyperlink] = {};

                if data not in rigid_descriptors[self.current_hyperlink]:
                    rigid_descriptors[self.current_hyperlink][data] = 1;
                else:
                    rigid_descriptors[self.current_hyperlink][data] += 1;

# parser to use to read data
parser = MyHTMLParser();

# go through all of the episodes
for i in range(1, NUM_EPS + 1):
    print("Downloading episode:", i);
    # construct request for this episode's wiki
    req = Request(URL_PREFIX + ("%03d" % i), headers={'User-Agent': 'Mozilla/5.0'});

    # read and parse wiki page
    with urlopen(req) as response:
        html = response.read();
        parser.feed(html.decode('UTF-8'));

# list of annotated strings
annotated = [];

# prepare annotated file for annotation
shutil.copy(RAW_TEXT_FILE, ANNOTATED_TEXT_FILE);
with open(ANNOTATED_TEXT_FILE, 'r') as file :
  filedata = file.read();

# English dictionary
d = enchant.Dict("en_US");

"""
Determines whether the given label is acceptable, and if so, adds the following
labels to the list of labels, given they are not already in the list
- the original label
- the label pluralized (adding an 's' to the end)
- the constituent words of the label that are not dictionary words
Current conditions:
- first letter of every word is uppercase or digit
- is not a possessive - does not end in "'s" 
- label has >1 characters 
"""
def process_label(label):
    # ignore possesives
    if label.endswith('\'s'):
        return;

    # do all of the words processed so far start with uppercase letters?
    all_valid_words = True;

    # check validity of all words
    words = label.split();
    for word in words:
        if not (word[0].isupper() or word[0].isdigit()):
            all_valid_words = False;

    # this is a valid descriptor
    if all_valid_words and (label not in annotated) and (len(label) > 1):
        annotated.append(label);

        # add the plural form as well
        plural_label = label + 's';
        if plural_label not in annotated:
            annotated.append(plural_label);

        for word in words:
            # ignore possesives
            if word.endswith('\'s'):
                return;

            # this is not a dictionary word
            if not d.check(word) and word not in annotated:
                annotated.append(word);

                # add the plural form as well
                plural_word = word + 's';
                if plural_word not in annotated:
                    annotated.append(plural_word);

# generate list of labels
for descriptor in rigid_descriptors:
    process_label(descriptor.strip());
    for label in rigid_descriptors[descriptor]:
        process_label(label.strip());

# sort from largest to smallest to ensure that substrings are annotated after
# the larger labels they are a part of (if we did not do this, annotating the
# substrings first would prevent detection of the larger strings they used to
# be a part of
annotated.sort(key = lambda x: len(x), reverse=True);

# annotate all matching labels
for label in annotated:
    # this name contains a period, so do a normal search and replace
    if label.find('.') != -1:
        filedata = re.sub( label, '[' + label + ']', filedata);
    # do a search and replace, ignoring substrings
    else:
        filedata = re.sub( r'\b%s\b' % re.escape(label), '[' + label + ']', filedata);

# write the file out again
with open(ANNOTATED_TEXT_FILE, 'w') as file:
  file.write(filedata)
