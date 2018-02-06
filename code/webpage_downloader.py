# File: webpage_downloader.py 
# Author(s): Rishikesh Vaishnav, Jessica Lacovelli, Bonnie Chen
# Created: 23/01/2018

from urllib.request import Request, urlopen;
from constants import *;

# total number of episodes in the first generation
NUM_EPS = 116;

# format string for episode numbers
EP_NUMBER_FORMAT = "%03d";

# go through all of the episodes
for i in range(1, NUM_EPS + 1):
    print("Downloading episode:", i);
    # construct request for this episode's wiki
    req = Request(URL_PREFIX + EP_PREFIX + (EP_NUMBER_FORMAT % i), headers={'User-Agent': 'Mozilla/5.0'});

    # download wiki page html
    with urlopen(req) as response:
        html = response.read();

        # write the file out to data folder
        with open(EP_WEBPAGE_DEST + (EP_NUMBER_FORMAT % i), 'w') as file:
          file.write(html.decode('UTF-8'));
