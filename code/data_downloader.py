# File: data_downloader.py 
# Author(s): Rishikesh Vaishnav, Jessica Lacovelli, Bonnie Chen
# Created: 23/01/2018

from urllib.request import Request, urlopen;
from html.parser import HTMLParser

PLOT_ATTRS = [('class', 'mw-headline'), ('id', 'Plot')];

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super(MyHTMLParser, self).__init__()
        self.parsing_plot = False;

    def handle_starttag(self, tag, attrs):
        if self.parsing_plot:
            if tag == 'h2':
                self.parsing_plot = False;
            else:
                print("start tag:", tag, "attributes:", attrs);
        elif self.is_plot_tag(attrs):
            self.parsing_plot = True;

    def is_plot_tag(self, attrs):
        plot_attr = True;
        for attr in PLOT_ATTRS:
            if attr not in attrs:
                plot_attr = False;

        return plot_attr;


    def handle_endtag(self, tag):
        if self.parsing_plot:
            print("end tag:", tag);

    def handle_data(self, data):
        if self.parsing_plot:
            print("data:", data);

f = open('temp', 'wb');

req = Request('https://bulbapedia.bulbagarden.net/wiki/EP001',headers={'User-Agent': 'Mozilla/5.0'});

parser = MyHTMLParser();

with urlopen(req) as response:
    html = response.read();
    f.write(html);
    parser.feed(html.decode('UTF-8'));
