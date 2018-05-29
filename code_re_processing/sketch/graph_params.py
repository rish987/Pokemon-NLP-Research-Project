# File: main.py 
# Author(s): Rishikesh Vaishnav, Jessica Iacovelli, Bonnie Chen
# Created: 29/05/2018
# Description:
#   Graph parameter objects for path correlation algorithm grapher.

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
    """
    def __init__(self, name, label):
        self.name = name;
        self.label = label;

    def get_name(self):
        return self.name;

    def get_label(self):
        return self.label;

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
Object representing a edge that is identified by two descriptors and a relation
between the descriptors. Has an edge weight representing the probability of
this relation existing between these descriptors.
"""
class Edge():
    """
    Initialize this edge.

    desc_sbj - the subject descriptor
    desc_obj - the object descriptor
    relation - the relation from 'desc_sbj' to 'desc_obj' that this relation
        represents
    """
    def __init__(self, desc_sbj, desc_obj, relation):
        self.desc_sbj = desc_sbj;
        self.desc_obj = desc_obj;
        self.relation = relation;

    def get_desc_sbj(self):
        return self.desc_sbj;

    def get_desc_obj(self):
        return self.desc_obj;

    def get_relation(self):
        return self.relation;
