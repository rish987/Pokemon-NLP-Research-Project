# File: pivot_conj_dict_generator.py 
# Author(s): Rishikesh Vaishnav, TODO
# Created: 15/02/2018
import json;
import chardet;
from constants import *;
from urllib.request import Request, urlopen;
from html.parser import HTMLParser;

PIVOT_URL_PREFIX = \
    r'http://conjugator.reverso.net/conjugation-english-verb-%s.html'

SIMPLE_FORMS_ATTR = 'ch_lblSimpleForms';
CONJ_STYLE_ATTR = 'font-style:normal;color:#003EAD';
SPAN_TAG = 'span';
I_TAG = 'i';

# class for processing HTML files of pivot conjugations
class PivotParser(HTMLParser):
    # add instance variables
    def __init__(self):
        super(PivotParser, self).__init__()
        self.parsing_simple_forms = False;
        self.parsing_i_in_simple_forms = False;
        self.conjs = [];

    def feed(self, html):
        self.conjs = [];
        super(PivotParser, self).feed(html);

    def handle_starttag(self, tag, attrs):
        if tag == SPAN_TAG:
            # encountered the next span, so no longer parsing the simple forms
            if self.parsing_simple_forms:
                self.parsing_simple_forms = False;
            else:
                id_attr = [x for x in attrs if x[0] == 'id'];
                if (len(id_attr) > 0) and (id_attr[0][1] == SIMPLE_FORMS_ATTR):
                    self.parsing_simple_forms = True;
        elif (tag == I_TAG) and (self.parsing_simple_forms):
            style_attr = [x for x in attrs if x[0] == 'style'];
            if (len(style_attr) > 0) and \
                (style_attr[0][1] == CONJ_STYLE_ATTR):
                self.parsing_i_in_simple_forms = True;

    def handle_endtag(self, tag):
        if (tag == I_TAG) and (self.parsing_i_in_simple_forms):
            self.parsing_i_in_simple_forms = False;

    def handle_data(self, data):
        if self.parsing_i_in_simple_forms and (data not in self.conjs):
            self.conjs.append(data);

    def get_conjs(self):
        return self.conjs;

# parser to use to read data
parser = PivotParser();

"""
Access the internet to find all conjugations of the given word.
"""
def get_conjs(word):
    # construct request for this episode's wiki
    req = Request(PIVOT_URL_PREFIX % word, \
        headers={'User-Agent': 'Mozilla/5.0'});

    # download wiki page html
    with urlopen(req) as response:
        html = response.read();

        parser.feed(html.decode('UTF-8'));

    return parser.get_conjs();

# load dictionary object
d = json.load(open('dictionary.json'));

# load raw data
filedata = '';
with open(RAW_TEXT_FILE, 'r') as file :
  filedata = file.read();

filedata = filedata.lower();

# to store mapping from verbs to their relevant conjugations
pivot_to_conjs = {};

i = 0;

num_words = len(d);

# go through all dictionary words
for word in d:
    # ignore this word if it has a space in it or cannot be converted to ascii
    if (' ' in word) or \
        (chardet.detect(bytes(word, 'utf-8'))['encoding'] != 'ascii'):
        #print("could not process word: " + word);
        continue;

    print(str(i) + '/' + str(num_words) + ': ' + word);
    # extract all definitions of this word
    defs = d[word]['definitions'];

    # all of the different parts of speech of this word
    pos_list = [defs[x]['part_of_speech'] for x in \
        range(len(defs))]


    # this word can be interpreted as a verb
    if ('verb' in pos_list):
        # get_conjs('anæsthetize');
        # get all possible conjugations of this verb
        conjs = get_conjs(word);

        # go through all conjugations
        for conj in conjs:
            conj = conj.strip();
            # this conjugation appears in the data
            if (re.search(r'\b%s\b' % conj.lower(), \
                filedata) != None):
                # create a new entry for this conjugation's originating word,
                # associating it with all of its conjugations
                pivot_to_conjs[word] = conjs;

                # no need to search for the next conjugation
                break;

    print(pivot_to_conjs);

    ## TODO increasing could improve accuracy
    #if i > 100:
    #    break;

    i += 1;

with open(PIVOT_CONJ_FILE, 'w') as file:
     file.write(json.dumps(pivot_to_conjs));
