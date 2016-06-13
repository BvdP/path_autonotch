#!/usr/bin/env python
from __future__ import division
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
            d = obj.get('d') # all the interesting stuff for SVG paths is in the 'd' attribute
            if d == None:
                doc.errormsg('Error: Selected object is not a path.')
                return
            path_str += d

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

        origin = doc.Coordinate(0, 0)
        endpoint = origin
        initial_point = None
        segments = []
        for pc in path_components:
            offset = origin if pc[1] else endpoint
            nr_args = len(pc[2])
            if nr_args % 2 == 0: # turns out that an even number of arguments means a list of x,y coordinates
                points = []
                for i in range(nr_args // 2):
                    points.append(doc.Coordinate(pc[2][2 * i], pc[2][2 * i + 1]))
            else: # elliptic arc
                points = [doc.Coordinate(pc[2][-2], pc[2][-1])] # only one coordinate for an arc

            points = [p + offset for p in points] # make all points absolute
            if initial_point is None:
                initial_point = points[0]

            if pc[0] == 'm':
                pass    # nothin to do: endpoint gets set later on
            if pc[0] == 'h':
                to = doc.Coordinate(pc[2][0] + offset, 0)
                segments.append(doc.Line(endpoint, to))
            if pc[0] == 'v':
                to = doc.Coordinate(0, pc[2][0] + offset)
                segments.append(doc.Line(endpoint, to))
            if pc[0] == 'l':
                segments.append(doc.Line(endpoint, points[0]))

            # note: up to now only tested with 'c', not sure if Inkscape generates the others
            if pc[0] in ('c', 'q', 's', 't') :
                pts = [endpoint]
                if pc[0] in ('s', 't') :
                    pts.extend(endpoint - last_control) # invert last Bezier control point
                pts.extend(points)
                segments.append(doc.BezierCurve(pts))
                last_control = points[-2]
            if pc[0] == 'a':
                rx, ry, x_rot, large_arc, sweep, x, y = pc[2]

                segments.append(doc.EllipticArc(endpoint, points[0], rx, ry, x_rot, sweep =='1', large_arc=='1'))
            if pc[0] == 'z':
                if endpoint != initial_point:
                    segments.append(doc.Line(endpoint, initial_point))
            else:
                endpoint = points[-1]

        root = self.document.getroot()
        for s in segments:
            #doc.errormsg(str(s.points))
            p = doc.Path()
            p.move_to(s.pathpoint_at_t(0).coord, True)
            for t in range(11):
                p.line_to(s.pathpoint_at_t(t/10).coord, True)
            p.path(root, doc.default_style)

# Create effect instance and apply it.
effect = Autonotch()
effect.affect()
