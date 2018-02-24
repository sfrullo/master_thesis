# coding: utf-8

import numpy as np

HEADER_LENGTH = 24

class GazeData(object):
    """docstring for GazeData"""
    def __init__(self, track):
        super(GazeData, self).__init__()
        self.track = track

    def load_gaze_from_file(self)
        print 'Load gaze file.'

        filename = self.track.get_filename()

        with open(filename, 'r') as f:
            # skip 24 lines
            for i in range(HEADER_LENGTH): f.readline()
            header = f.readfline().replace('\n', '').split('\t')
            data = {h:[] for h in header}
            for line in f:
                [ data[header[i]].append(d) for i,d in enumerate(line.split('\t')) ]

        self.header = header
        self.data = data

        print self.header
        print self.data