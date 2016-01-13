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
            ['default_diameter', 'float', '60', 'Default diameter'],
            ['curve_factor', 'float', '2', 'Curvature factor']
        ]
        doc.Effect.__init__(self, options)

    def effect(self):
        """
        Blah.
        """
        path_commands = { # uppercase commands == absolute coordinates
            'm':2, # moveto
            'l':2, # lineto
            'h':1, # horizontal lineto
            'v':1, # vertical ...
            'c':6, # cuveto (cubic Bezier)
            's':4, # smooth curveto (1st control point is reflection of 2nd cp of previous segment)
            'q':4, # quadratic Bezier curveto
            't':2, # smooth quadratic Bezier ...
            'a':7, # elliptical arc to
            'z':0  # close path
        }
        path_str = ''
        for name, obj in self.selected.iteritems():
            path_str += obj.get('d') # all the interesting stuff for SVG paths is in the 'd' attribute

        path_items = path_str.replace(',', ' ').split()
        path_items = [float(x) if not x.isalpha() else x for x in path_items]
        i = 0
        path_components = []
        while i < len(path_items):
            if not isinstance(path_items[i], float):
                command = path_items[i]
                nr_args = path_commands[command.lower()]
                i += 1
            path_components.append((command.lower(), command.isupper(), path_items[i:i + nr_args]))
            i += nr_args
        doc.errormsg(str(path_components))

        for pc in path_components:
            pass




# Create effect instance and apply it.
effect = Autonotch()
effect.affect()