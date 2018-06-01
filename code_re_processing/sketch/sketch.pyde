# File: sketch.pyde
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen
# Created: 29/05/2018
# Description:
#   Main executable for path correlation algorithm grapher.
from setup import load_graph_params, GRAPH_PARAM_FOLDER;
from graph_params import *;
import random;
import math;

# TODO
labels, descriptors, relations, relation_instances = \
     load_graph_params(GRAPH_PARAM_FOLDER);

"""
Sets up the canvas.
"""
def setup():
    size(CANVAS_WIDTH, CANVAS_HEIGHT);

    strokeWeight(2);

    # use white background
    background(255);

# number of edges to draw TODO remove
NUM_EDGES = 3;

"""
Draws on the canvas.
"""
def draw():
    draw_graph = True;
    if draw_graph:
        # draw all relation_instances/edges
        for edge_i_div in range(NUM_EDGES):
            edge_i = (edge_i_div * 10) + 1
            relation_instances[edge_i].set_probability(random.random());
            relation_instances[edge_i].draw();

        # draw all descriptors/nodes
        for descriptor in descriptors:
            descriptor.draw();

    delay(100);
