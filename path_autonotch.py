#!/usr/bin/env python

import Inkscape_helper.inkscape_helper as doc

class Autonotch(doc.Effect):
    """
    Creates notched edges for the selected curve
    """
    def __init__(self):

        options = [#['selected_tab', 'string'],
            ['unit', 'string', 'mm', 'Unit (mm, cm, px, in, ft, ...)'],
            ['thickness', 'float', '3', 'Material thickness'],
            ['depth', 'float', '80.0', 'Depth'],
            ['tab_size', 'float', '10', 'Approximate tab for straight sections (tabs will be evenly spaced along the length of the edge)'],
            ['cut_dist', 'float', '2.0', 'Distance between cuts on the rounded corners. Note that this value will change slightly to evenly fill up the available space.'],
            ['cut_nr', 'int', '3', 'Number of cuts across the depth.'],
            ['curve_factor', 'float', '2', 'Curvature factor']
        ]
        doc.Effect.__init__(self, options)

    def effect(self):
        """
        Blah.
        """
        path_commands = {'m':2, 'l': 2, 'h':1, 'v':1, 'c':6, 's':4, 'q':4, 't':2, 'a':7, 'z':0} # lowercase commands and the corresponding number of arguments
        path_str = ''
        for name, obj in self.selected.iteritems():
            path_str += obj.get('d') # all the interesting stuff for SVG paths is in the 'd' attribute

        path_items = path_str.replace(',', ' ').split()
        path_items = [float(x) if not x.isalpha() else x for x in path_items]
        doc.errormsg(str(path_items))


# Create effect instance and apply it.
effect = Autonotch()
effect.affect()