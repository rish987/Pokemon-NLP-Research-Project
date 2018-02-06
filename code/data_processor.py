# File: data_processor.py 
# Author(s): Rishikesh Vaishnav, Jessica Lacovelli, Bonnie Chen
# Created: 23/01/2018
# Description: Processes HTML data from to extract relevant information.
# Usage:
# $ python data_processor.py [annotate]
# - [annotate]: '1' if want to annotate, omitted or anything else if do not
# want to annotate

# TODO address beginning/ending of sentences when finding surrounding words

from urllib.request import Request, urlopen;
from html.parser import HTMLParser;
import re;
import enchant;
import shutil;
import sys;
import os.path;

from constants import *;

# expected tag and attributes of plot header
PLOT_TAG = 'span'
PLOT_ATTRS = [('class', 'mw-headline'), ('id', 'Plot')];

# tag used for hyperlink
LINK_TAG = 'a'

# total number of episodes in the first generation
NUM_EPS = 116;

# regular expression to remove parentheses from a string
REMOVE_PARENS_REGEX = r'\([^)]*\)';

# files to write data to
raw_text_file = open(RAW_TEXT_FILE, 'w');

# list of entities found
entities = [];

# special characters that could be part of a descriptor
SPECIAL_CHARACTERS = ['.'];

# words to be ignored when checking capitalization
IGNORED_WORDS = ['a', 'an', 'the', 'and', 'but', 'for', 'of', 'with'];

# data folder webpages
ENTITY_WEBPAGE_DEST = '../data/webpages/entities/';
EP_WEBPAGE_DEST = '../data/webpages/episodes/';

# format string for episode numbers
EP_NUMBER_FORMAT = '%03d';

# string to match descriptor, in its plural forms as well (ending in 'es' or
# 's'), both separate and unseparate from other words
DESCRIPTOR_FORMAT_SEPARATE = r'(\b%s(?:e?s)?\b)';
DESCRIPTOR_FORMAT_UNSEPARATE = r'(%s(?:e?s)?)';

DESCRIPTOR_FORMAT_SURROUNDING = r'\w+ \w+ %s \w+ \w+'

# suffixes for pluralized descriptors
PLURAL_SUFFIXES = ['s', 'es'];

# check if we should annotate data
annotate = False;
if (len(sys.argv) > 1) and (sys.argv[1] == '1'):
    annotate = True;

# check if we should download entity data
download_entities = False;
if (len(sys.argv) > 2) and (sys.argv[2] == '1'):
    download_entities = True;

# alternate names for labels
label_altnames = { 'pokemon': ['pokémon  category', 'legendary pokémon', 'color pokémon', 'caught pokémon', 'type pokémon', '\'s pokémon', 's\' pokémon', 'starter pokémon', 'starter pokemon', 'colored pokémon', 'pokémon with', 'primeape', 'wild pokémon', 'ho-oh', 'group pokémon'], 'person': ['person', 'character', 'trainer', 'professor', 'nurse', 'member', 'gym leader', 'twerp', 'father', 'mother', 'mayor'], 'settlement': ['city', 'town', 'village'], 'move': ['move', 'attack'], 'event':['event', 'battle', 'contest', 'competition', 'festival', 'party', 'conference'], 'item': ['item', 'badge', 'ball', 'potion', 'bike', 'equipment', 'technology', 'mecha', 'movie', 'berry', 'trophy', 'food'], 'region': ['region', 'area', 'zone', 'location'], 'concept': ['concept', 'title', 'motto', 'running gag', 'physics', 'meta', 'episode', 'mechanic', 'pokémon training', 'journey', 'narrator', 'transportation'], 'building':['building', 'center', 'gym', 'house', 'tower', 'hall', 'palace', 'laboratory', 'institute'], 'group':['groups', 'league', 'trio', 'duo', 'cheerleaders', 'squad', 'organization'], 'type': ['types'], 'condition':['conditions']};

# emphasized altnames - if these are in the categories, it's almost certain to 
# be of the corresponding label
emphasized_altnames = ['\'s pokémon', 's\' pokémon', 'groups', 'building', 'town', 'region', 'squad', 'mecha']

# class for processing HTML files
class LabelParser(HTMLParser):
    # add instance variables
    def __init__(self):
        super(LabelParser, self).__init__()
        # is the categories section currently being parsed?
        self.in_categories = False;

    def feed(self, html, title):
        self.title = title;
        super(LabelParser, self).feed(html);

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            title_attrs = [attr for attr in attrs if attr[0] == 'title'];
            if len(title_attrs) > 0:
                # just entered categories section
                if title_attrs[0][1] == 'Special:Categories':
                    self.in_categories = True;
                    self.label_points = {};
                    self.categories_data = self.title + ' ';
            
    def handle_endtag(self, tag):
        # just ended a categories section
        if tag == 'div' and self.in_categories:
            self.in_categories = False;
            # determine the label of this entity
            self.determine_label(self.categories_data);

    def determine_label(self, text):
        text = text.lower();
        # go through all names
        for label in label_altnames:
            for altname in label_altnames[label]:
                loc = text.find(altname.lower());
                if loc > -1:
                    # assign points to this label such that categories that
                    # appear earlier on get more points, and emphasized labels
                    # get extra points
                    points = len(text) - loc;
                    if label not in self.label_points:
                        self.label_points[label] = 0;
                    if altname in emphasized_altnames:
                        points = points * 10;
                    self.label_points[label] += points;

        best_label = 'No match.'
        best_label_points = 0;

        for label in self.label_points:
            if self.label_points[label] > best_label_points:
                best_label_points = self.label_points[label];
                best_label = label;

        if best_label == 'No match.':
            print("NO MATCH: " + text);

        self.label = best_label;

    def handle_data(self, data):
        if self.in_categories:
            # add this category description to the growing string
            self.categories_data += data;

    def get_label(self):
        return self.label;

# parser to use to determine labels
label_parser = LabelParser();

# data structure for storing entity information
class Entity():
    # initiates this entity with the given official title and link to wiki page
    def __init__(self, _title, _link):
        self.title = _title;
        self.link = _link;
        self.altnames = [];
        self.label = '';
        self.words = {};

        # add the title as an initial altname 
        self.altnames.append(_title);

        self.determine_label();

    # adds the specified altname to this Entity's list of altnames if it's not
    # already added
    def add_altname(self, altname):
        if altname not in self.altnames:
            self.altnames.append(altname);

    # removes the specified altname to this Entity's list of altnames
    def remove_altname(self, altname):
        if altname in self.altnames:
            self.altnames.remove(altname);

    # returns the title of this entity
    def get_title(self):
        return self.title;

    # returns the full link to this entity's wiki page
    def get_link(self):
        return URL_PREFIX + self.link;

    # returns this entity's altnames
    def get_altnames(self):
        return self.altnames;

    # determines the label of this entity
    def determine_label(self):
        if not self.link[0] == '/':
            self.label = 'None';
            return;
        filename = ENTITY_WEBPAGE_DEST + self.link.replace('/', '_');
        file_exists = os.path.isfile(filename);
        if not file_exists or download_entities:
            # construct request for this episode's wiki
            req = Request(URL_PREFIX + self.link, headers={'User-Agent': 'Mozilla/5.0'});
            # download wiki page html
            with urlopen(req) as response:
                html = response.read();

                with open(filename, 'w') as file :
                  file.write(html.decode('UTF-8'));

                label_parser.feed(html.decode('UTF-8'), self.title);
        else:
            with open(filename, 'r') as file :
                label_parser.feed(file.read(), self.title);

        self.label = label_parser.get_label();

        # TODO
        #print("Labeled: \t" + self.title + "\t" + self.label);

    # returns the label of this entity
    def get_label(self):
        return self.label;

# class for processing HTML files
class EpisodeParser(HTMLParser):
    # add instance variables
    def __init__(self):
        super(EpisodeParser, self).__init__()
        self.parsing_plot = False;
        self.just_seen_plot_tag = False;
        self.in_hyperlink = False;
        self.current_hyperlink_title = '';
        self.current_hyperlink_link = '';

    def handle_starttag(self, tag, attrs):
        if self.parsing_plot:
            # this is a new header seen while parsing under the plot header, so
            # the plot description must be over
            if tag == PLOT_TAG:
                self.parsing_plot = False;

            elif tag == LINK_TAG:
                title_attr = [x for x in attrs if x[0] == 'title'];
                link_attr = [x for x in attrs if x[0] == 'href'];
                if (len(title_attr) > 0) and (len(link_attr) > 0):
                    # indicate that currently parsing hyperlink
                    self.in_hyperlink = True;
                    # set current hyperlink
                    self.current_hyperlink_title = re.sub(REMOVE_PARENS_REGEX, '', title_attr[0][1]);
                    self.current_hyperlink_link = link_attr[0][1];
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
                matching_entities = [e for e in entities if e.get_title() == self.current_hyperlink_title];
                matching_entity = '';

                # a matching entity does not already exist, so make a new one
                if len(matching_entities) == 0:
                    matching_entity = Entity(self.current_hyperlink_title, self.current_hyperlink_link);
                    entities.append(matching_entity);
                else:
                    # there should be only a single match
                    matching_entity = matching_entities[0];

                # add this data to this entity's list of altnames
                matching_entity.add_altname(data);

# parser to use to read data
parser = EpisodeParser();

# go through all of the episodes
for i in range(1, NUM_EPS + 1):
    print('Processing episode:', i);

    # open the downloaded webpage file
    with open(EP_WEBPAGE_DEST + (EP_NUMBER_FORMAT % i), 'r') as file:
        parser.feed(file.read());

# dictionary of used descriptors to their entities
descriptors = {};

if annotate:
    # prepare annotated file for annotation
    shutil.copyfile(RAW_TEXT_FILE, ANNOTATED_TEXT_FILE);

with open(RAW_TEXT_FILE, 'r') as file :
  filedata = file.read();

# English dictionary
d = enchant.Dict('en_US');

"""
Determines whether the given altname is acceptable, and if so, adds the
following altnames to the list of altnames, given they are not already in the
list
- the original altname
- the constituent words of the altname that are not dictionary words
Current conditions:
- first letter of every word is uppercase or digit, unless the word is a word
  that is conventionally uncapitalized in English descriptors
- altname has >1 characters 
"""
def process_altname(altname, entity):
    # ignore possesives
    if altname.endswith('\'s'):
        altname = altname[:-2];

    # do all of the words processed so far start with uppercase letters?
    all_valid_words = True;

    # check validity of all words
    words = altname.split();
    for word in words:
        if not ((word in IGNORED_WORDS) or word[0].isupper() or word[0].isdigit()):
            all_valid_words = False;

    # this is a valid descriptor
    if all_valid_words and (altname not in descriptors) and (len(altname) > 1):
        descriptors[altname] = entity;

        for word in words:
            # ignore possesives
            if word.endswith('\'s'):
                word = word[:-2];

            # this is not a dictionary word
            if not d.check(word) and word not in descriptors:
                descriptors[word] = entity;

print('Finding all potential altnames...');

# clear out all plurals
for entity in entities:
    altnames = entity.get_altnames();
    for altname in altnames:
        for suffix in PLURAL_SUFFIXES:
            plurals = [n for n in altnames if n == altname + suffix];
            for plural in plurals:
                entity.remove_altname(plural);
        
# generate list of altnames
for entity in entities:
    for altname in entity.get_altnames():
        process_altname(altname.strip(), entity);

# sort from largest to smallest to ensure that substrings are annotated after
# the larger altnames they are a part of (if we did not do this, annotating the
# substrings first would prevent detection of the larger strings they used to
# be a part of
descriptors_sorted = sorted(descriptors, key = lambda x: len(x), reverse=True);

if annotate:
    # to store data with this name annotated
    filedata_new = filedata;

    print('Annotating...');
    # annotate all matching altnames
    for altname in descriptors_sorted:

        # this name contains a period, so do a normal search and replace
        if altname.find('.') != -1:
            filedata_new = re.sub( DESCRIPTOR_FORMAT_UNSEPARATE % re.escape(altname), r'[\1]', filedata_new);
        # do a search and replace, ignoring substrings
        else:
            filedata_new = re.sub( DESCRIPTOR_FORMAT_SEPARATE % re.escape(altname), r'[\1]', filedata_new);


    # write the annotated file
    with open(ANNOTATED_TEXT_FILE, 'w') as file:
      file.write(filedata_new)

print('Removing unused descriptors...');

# list of items to remove from descriptors_sorted
remove_list = [];

# identify all unused descriptors_sorted
for descriptor in descriptors_sorted:
    search = None;

    # this name contains a period, so do a normal search
    if descriptor.find('.') != -1:
        search = re.search( DESCRIPTOR_FORMAT_UNSEPARATE % re.escape(descriptor), filedata);
    # do a search, ignoring substrings
    else:
        search = re.search( DESCRIPTOR_FORMAT_SEPARATE % re.escape(descriptor), filedata);

    # no instance of this descriptor was found in the actual text
    if search == None:
        remove_list.append(descriptor);

# identify all unused descriptors
for to_remove in remove_list:
    descriptors_sorted.remove(to_remove);

with open(DESCRIPTORS_FILE, 'w') as file:
    for d in descriptors_sorted:
        file.write(d + '\n');

with open(LABELED_DESCRIPTORS_FILE, 'w') as file:
    for d in descriptors_sorted:
        file.write(descriptors[d].get_label() + '\t\t' + d + '\n');

# print("Identifying surrounding words...");
# 
# descriptor_to_surroundings = {};
# 
# for descriptor in descriptors_sorted:
#     found = re.findall( DESCRIPTOR_FORMAT_SURROUNDING % re.escape(entry), filedata);
#     entity = descriptor_to_entity[entry];
#     entity.process_context_strings(found);
