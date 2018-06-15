# coding: utf-8

# native
import os
import os.path as path

# external
import numpy as np
import matplotlib.pyplot as plt

# custom
import emosm.tools.utils as utils
import emosm.sm.basesm as basesm
import emosm.dataset.mahnob.config as config

class GazeSaliencyMap(basesm.BaseSaliencyMap):
    """docstring for GazeSaliencyMap"""
    def __init__(self, gaze_data=None, *arg, **kwarg):
        super(GazeSaliencyMap, self).__init__()
        self.gaze_data = gaze_data

    def compute_saliency_map(self, limit_frame=None, display_size=None):
        print "start compute saliency map"

        if display_size is None:
            raise ValueError("display_size must be a tuple")

        fixations = self.gaze_data['fixations'] / config.FRAME_SCALE_FACTOR
        total_fixations_sample = self.gaze_data['fixations'].shape[0]

        if limit_frame is not None:
            fixations = fixations[:limit_frame]

        framed_sample_generator = utils.moving_window_data_per_frame_generator(fixations, ws=config.MIN_SAMPLE_WINDOW)

        print "Process frame"
        for frame_number, framed_sample in enumerate(framed_sample_generator):
            print "#{}".format(frame_number)
            frame_heatmap = self.compute_frame_saliency_map(framed_sample, display_size)
            yield frame_heatmap
        print "End"