# File: main.py 
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen
# Created: 29/05/2018
# Description:
#   Graph parameter objects and constants for path correlation algorithm
#   grapher.
import math;

# - canvas parameters -
CANVAS_WIDTH = 500;
CANVAS_HEIGHT = 500;
# -

# - grid parameters -
# number of grid columns
GRID_COLS = 15

# number of grid rows
GRID_ROWS = 15

# pixel width and height of rows and columns
COLUMN_WIDTH = int(CANVAS_WIDTH / GRID_COLS)
ROW_HEIGHT = int(CANVAS_HEIGHT / GRID_ROWS)
# -

# - node parameters -
# radius of nodes
NODE_RADIUS = 15;

# grayscale color of node fill
NODE_FILL_COLOR = 200;

# grayscale color of node borders
NODE_STROKE_COLOR = 0;

# grayscale color of node text
NODE_TEXT_FILL_STROKE_COLOR = 0;

# node text font side
NODE_TEXT_SIZE = 10;
# -

"""
Object representing a label that is identified by name.
"""
class Label():
    """
    Initialize this label.

    name - the name of this label
    """
    def __init__(self, name):
        self.name = name;

    def get_name(self):
        return self.name;


"""
Object representing a descriptor that is identified by a name and a label.
"""
class Descriptor():
    """
    Initialize this descriptor.

    name - the name of this descriptor
    label - the label of this descriptor
    
    x - (graphing parameter, optional) the column position of this descriptor
    y - (graphing parameter, optional) the row position of this descriptor
    """
    def __init__(self, name, label, x=0, y=0):
        self.name = name;
        self.label = label;

        self.x = x;
        self.y = y;

    """
    Set the x- and y-position of this label;
    """
    def set_pos(self, x, y):
        self.x = x;
        self.y = y;

    def get_name(self):
        return self.name;

    def get_label(self):
        return self.label;

    # - graphing functions -
    def get_x_grid(self):
        return int(self.x * COLUMN_WIDTH)

    def get_y_grid(self):
        return int(self.y * ROW_HEIGHT)

    def get_x(self):
        return self.x;

    def get_y(self):
        return self.y;

    def draw(self):
        # - draw node -
        fill(NODE_FILL_COLOR);
        stroke(NODE_STROKE_COLOR);
        x_pos = (self.x * COLUMN_WIDTH);
        y_pos = (self.y * ROW_HEIGHT);
        ellipse(x_pos, y_pos, NODE_RADIUS * 2, NODE_RADIUS * 2);
        # -

        # - draw text -
        fill(NODE_TEXT_FILL_STROKE_COLOR);
        stroke(NODE_TEXT_FILL_STROKE_COLOR);
        textSize(NODE_TEXT_SIZE);
        text_width_name = textWidth(self.name);
        text(self.name, x_pos - int(text_width_name / 2), y_pos);
        text_width_label = textWidth(self.label.get_name());
        text(self.label.get_name(), x_pos - int(text_width_label / 2), \
            y_pos + 10);
        # -
    # -

"""
Object representing a relation that is identified by name.
"""
class Relation():
    """
    Initialize this relation.

    name - the name of this relation
    """
    def __init__(self, name):
        self.name = name;

    def get_name(self):
        return self.name;

"""
Object representing a relation instance that is identified by two descriptors
and a relation between the descriptors. Has a number representing the
probability of this relation existing between these descriptors.
"""
class RelationInstance():
    """
    Initialize this relation instance.

    desc_sbj - the subject descriptor
    desc_obj - the object descriptor
    relation - the relation from 'desc_sbj' to 'desc_obj' that this relation
    instance represents
    """
    def __init__(self, desc_sbj, desc_obj, relation):
        self.desc_sbj = desc_sbj;
        self.desc_obj = desc_obj;
        self.relation = relation;
        self.probability = 0.0;

    def get_desc_sbj(self):
        return self.desc_sbj;

    def get_desc_obj(self):
        return self.desc_obj;

    def get_probability(self):
        return self.probability;

    def set_probability(self, probability):
        self.probability = probability;

    def get_relation(self):
        return self.relation;

    # - graphing functions -
    def draw(self):
        # - draw arrow -
        drawArrow( self.desc_sbj.get_x_grid(), self.desc_sbj.get_y_grid(),\
                self.desc_obj.get_x_grid(), self.desc_obj.get_y_grid(),\
                NODE_RADIUS, int(255 * (1.0 - self.probability)));
        # -

        # - draw text TODO -
#        fill(NODE_TEXT_FILL_STROKE_COLOR);
#        stroke(NODE_TEXT_FILL_STROKE_COLOR);
#        textSize(NODE_TEXT_SIZE);
#        text_width_name = textWidth(self.name);
#        text(self.name, x_pos - int(text_width_name / 2), y_pos);
#        text_width_label = textWidth(self.label.get_name());
#        text(self.label.get_name(), x_pos - int(text_width_label / 2), \
#            y_pos + 10);
        # -
    # -

def drawArrow(start_x, start_y, end_x, end_y, radius, color):
    stroke(color);
    line(start_x, start_y, end_x, end_y);
    
    # difference in x- and y-directions
    diff_y = start_y - end_y;
    diff_x = start_x - end_x;

    angle = math.atan2(diff_y, diff_x);

    # x- and y- offsets of triangle
    x_off = radius * math.cos(angle);
    y_off = radius * math.sin(angle);

    fill(color);
    stroke(color);
    ellipse(end_x - x_off, end_y - y_off, 4, 4);

