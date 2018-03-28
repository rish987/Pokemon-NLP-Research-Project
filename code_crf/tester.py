# File: tester.py 
# Author(s): Rishikesh Vaishnav, TODO
# Created: 28/03/2018
import utilities;
import re;
from constants import *;

sentence = 'As Ash arrives in Viridian City, he is stopped by an Officer\
Jenny, who gives him a ride to the Pokémon Center after his Pokédex confirms\
his identity.'
search_term = 'Ash';

r = re.compile(descriptor_regex % re.escape(search_term));
iterator = r.finditer(sentence);
for match in iterator:
    print(match.span());
