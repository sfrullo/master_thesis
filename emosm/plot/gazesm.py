# coding: utf-8

# native
import os
import os.path as path

# external
import numpy as np

# custom
import emosm.tools.utils as utils
import emosm.dataset.mahnob.config as config


class GazeSaliencyMap(object):
    """docstring for GazeSaliencyMap"""
    def __init__(self, gaze_data=None, media=None, *arg, **kwarg):
        super(GazeSaliencyMap, self).__init__()
        self.gaze_data = gaze_data
        self.media = media

    def set_gaze_data(self, gaze_data):
        self.gaze_data = gaze_data

    def set_media(self, media):
        self.media = media

    def compute_saliency_map(self):
        print self.gaze_data
        print self.media