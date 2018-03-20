# coding: utf-8

class GazeSaliencyMap(object):
    """docstring for GazeSaliencyMap"""
    def __init__(self, gaze_data, media=None, *arg, **kwarg):
        super(GazeSaliencyMap, self).__init__()
        self.gaze_data = gaze_data

        if media is not None:
            self.media = media


        print self.gaze_data
        print self.media