# File: sketch.pyde
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen
# Created: 29/05/2018
# Description:
#   Main executable for path correlation algorithm grapher.
from setup import load_graph_params, GRAPH_PARAM_FOLDER;
from graph_params import *;
import random;

# TODO
labels, descriptors, relations, relation_instances = \
     load_graph_params(GRAPH_PARAM_FOLDER);

descriptor_i = 0;
## set position for all descriptors
#for descriptor in descriptors:
#    descriptor.set_pos((descriptor_i % GRID_COLS) + 1,\
#                       int(descriptor_i / GRID_COLS) + 1);
#    descriptor_i += 1;
# TODO


"""
Sets up the canvas.
"""
def setup():
    size(CANVAS_WIDTH, CANVAS_HEIGHT);

    # use white background
    background(255);

"""
Draws on the canvas.
"""
def draw():
    # draw all relation_instances/edges
    for relation_instance in relation_instances:
        relation_instance.set_probability(random.random());
        relation_instance.draw();

    # draw all descriptors/nodes
    for descriptor in descriptors:
        descriptor.draw();

    delay(100);
