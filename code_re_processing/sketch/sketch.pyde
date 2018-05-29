# File: main.py 
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen
# Created: 29/05/2018
# Description:
#   Main executable for path correlation algorithm grapher.
from setup import load_graph_params, GRAPH_PARAM_FOLDER;
from graph_params import Label, Descriptor, Relation;

# - grid parameters -
# number of grid columns
GRID_COLS = 50

# number of grid rows
GRID_ROWS = 50
# -

# - node parameters -
# radius of nodes
NODE_RADIUS = 10;

# grayscale color of node fill
NODE_FILL_COLOR = 200;

# grayscale color of node borders
NODE_STROKE_COLOR = 0;

# grayscale color of node text
NODE_TEXT_FILL_STROKE_COLOR = 0;
# -

# TODO
test = load_graph_params(GRAPH_PARAM_FOLDER);
# TODO

"""
Sets up the canvas.
"""
def setup():
    size(500, 500);

    # use white background
    background(255);

"""
Draws on the canvas.
"""
def draw():
    fill(NODE_FILL_COLOR);
    stroke(NODE_STROKE_COLOR);
    ellipse(50, 50, NODE_RADIUS * 2, NODE_RADIUS * 2);
