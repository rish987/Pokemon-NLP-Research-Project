# File: data_downloader.py 
# Author(s): Rishikesh Vaishnav, Jessica Lacovelli, Bonnie Chen
# Created: 23/01/2018

from urllib.request import Request, urlopen;
from html.parser import HTMLParser
import re
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
                # TODO set current_hyperlink
            # this is a section under the plot header; want to capture this
            # data
            else:
                # TODO process data
                pass;
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

for descriptor in rigid_descriptors:
    if descriptor[0].isupper() and descriptor not in annotated:
        annotated.append(descriptor.strip());
    for label in rigid_descriptors[descriptor]:
        # NOTE: only considering labels longer than 1 letter, starting with 
        # capital letters
        if label[0].isupper() and label not in annotated and len(label) > 1:
            annotated.append(label.strip());

annotated.sort(key = lambda x: len(x), reverse=True);

for label in annotated:
    filedata = filedata.replace(label, '[' + label + ']');

# Write the file out again
with open(ANNOTATED_TEXT_FILE, 'w') as file:
  file.write(filedata)
