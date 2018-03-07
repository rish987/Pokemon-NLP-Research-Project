# File: data_processor.py 
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen
# Created: 23/01/2018
# Description: Processes HTML webpages to extract text descriptions.
from urllib.request import Request, urlopen;
from html.parser import HTMLParser;
from constants import *;

# expected tag and attributes of plot headers in webpage HTML
PLOT_TAG = 'span'
PLOT_ATTRS = [('class', 'mw-headline'), ('id', 'Plot')];

# tag used for hyperlink
LINK_TAG = 'a'

# location of HTML files
EPISODE_WEBPAGE_FOLDER = '../data/webpages/episodes/';

# class for processing HTML files of episodes
class EpisodeParser(HTMLParser):
    # add instance variables
    def __init__(self):
        super(EpisodeParser, self).__init__()
        self.parsing_plot = False;
        self.just_seen_plot_tag = False;
        self.in_hyperlink = False;
        self.text_file = None;

    def feed_with_ep_num(self, read_file, ep_num):
        # open file to write data to
        self.text_file = open(TEXT_FOLDER + (EP_NUMBER_FORMAT % ep_num), 'w');
        self.feed(read_file);

    def handle_starttag(self, tag, attrs):
        if self.parsing_plot:
            # this is a new header seen while parsing under the plot header, so
            # the plot description must be over
            if tag == PLOT_TAG:
                self.parsing_plot = False;

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

    def handle_data(self, data):
        if self.parsing_plot:
            data = data.replace('\n', '');
            self.text_file.write(data);

# parser to use to read data
parser = EpisodeParser();

# go through all of the episodes
for i in range(1, NUM_EPS + 1):
    print('Processing episode: ' + str(i));
    
    # open the downloaded webpage file
    with open(EPISODE_WEBPAGE_FOLDER + (EP_NUMBER_FORMAT % i), 'r') as file:
        parser.feed_with_ep_num(file.read(), i);
