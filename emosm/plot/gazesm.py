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
    def __init__(self, *arg, **kwarg):
        super(GazeSaliencyMap, self).__init__()
        self.gaze_data = None

    def set_gaze_data(self, gaze_data):
        self.gaze_data = gaze_data

    def compute_saliency_map(self):
        pass

    def export_plot_on_media(self, media=None, filename=None):

        if media is None:
            raise ValueError("You must pass a Media object")

        if filename is None:
            media_name = path.splitext(path.basename(media.filename))[0]
            filename = "gm_" + media_name + ".mp4"

        media_fps = media.metadata["fps"]
        chunk_size = config.SAMPLE_RATE / media_fps

        print media_fps
        print chunk_size