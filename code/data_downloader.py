# File: data_downloader.py 
# Author(s): Rishikesh Vaishnav, Jessica Lacovelli, Bonnie Chen
# Created: 23/01/2018

from urllib.request import Request, urlopen;
from html.parser import HTMLParser

# expected tag and attributes of plot header
PLOT_TAG = 'span'
PLOT_ATTRS = [('class', 'mw-headline'), ('id', 'Plot')];

# total number of episodes in the first generation
NUM_EPS = 116;

# bulbapedia wiki URL prefix
URL_PREFIX = 'https://bulbapedia.bulbagarden.net/wiki/EP';

# file to write data to
f = open('../data/data.txt', 'w');

# class for processing HTML files
class MyHTMLParser(HTMLParser):
    # add instance variables
    def __init__(self):
        super(MyHTMLParser, self).__init__()
        self.parsing_plot = False;
        self.just_seen_plot_tag = False;

    def handle_starttag(self, tag, attrs):
        if self.parsing_plot:
            # this is a new header seen while parsing under the plot header, so
            # the plot description must be over
            if tag == PLOT_TAG:
                self.parsing_plot = False;
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
        if self.just_seen_plot_tag and (tag == PLOT_TAG):
            self.parsing_plot = True;
            self.just_seen_plot_tag = False;
        elif self.parsing_plot:
            # TODO process
            pass;

    def handle_data(self, data):
        if self.parsing_plot:
            f.write(data);

# parser to use to read data
parser = MyHTMLParser();

# go through all of the episodes
for i in range(1, NUM_EPS + 1):
    print(i);
    # construct request for this episode's wiki
    req = Request(URL_PREFIX + ("%03d" % i), headers={'User-Agent': 'Mozilla/5.0'});

    # read and parse wiki page
    with urlopen(req) as response:
        html = response.read();
        parser.feed(html.decode('UTF-8'));
