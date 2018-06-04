# coding: utf-8

# native
import os
import os.path as path

# external
import numpy as np
import matplotlib.pyplot as plt

# custom
import emosm.tools.utils as utils
import emosm.dataset.mahnob.config as config


class GazeSaliencyMap(object):
    """docstring for GazeSaliencyMap"""
    def __init__(self, gaze_data=None, media=None, *arg, **kwarg):
        super(GazeSaliencyMap, self).__init__()
        self.gaze_data = gaze_data
        self.media = media

        self.gwh = config.GAUSSIAN_WIDTH
        self.gsdwh = config.GAUSSIAN_STD_DEV
        self.gaus = utils.gaussian(self.gwh, self.gsdwh)

    def set_gaze_data(self, gaze_data):
        self.gaze_data = gaze_data

    def set_media(self, media):
        self.media = media

    def __compute_frame_saliency_map(self, fixations, display_size, mean_data=None, normalize=True):

        n_samples, data_dim = fixations.shape

        # mean fixations in case of multiple sessions
        if mean_data is None:
            X, Y, D = fixations.T
        else:
            X, Y, D = fixations.mean(axis=0)

        x0 = y0 = 0
        x1, y1 = display_size
        w, h = display_size
        data = zip(X, Y, D)

        heatmap = utils.grid_density_gaussian_filter(x0, y0, x1, y1, w, h, fixations)

        if normalize is True:
            heatmap *= 1/heatmap.max()

        return heatmap

    def compute_saliency_map(self, limit_frame=None):
        print "start compute saliency map"

        fixations = self.gaze_data['fixations'] / config.FRAME_SCALE_FACTOR
        total_fixations_sample = self.gaze_data['fixations'].shape[0]

        scale_media = config.SCALE_MEDIA
        display_size = self.media.get_size(scaled=scale_media)

        n_frames = self.media.metadata['nframes']

        sample_per_frame = np.floor(total_fixations_sample / float(n_frames))

        if limit_frame is not None:
            stop = int(limit_frame * sample_per_frame)
            fixations = fixations[0:stop]

        framed_sample_generator = utils.moving_window_data_per_frame_generator(fixations, spf=sample_per_frame, ws=config.MIN_SAMPLE_WINDOW)
        media_frame = self.media.get_frames(limit_frame=limit_frame, scale=scale_media)

        print "Process frame"
        for frame_number, (framed_sample, frame) in enumerate(zip(framed_sample_generator, media_frame)):
            print "#{}".format(frame_number)
            frame_heatmap = self.__compute_frame_saliency_map(framed_sample, display_size)
            yield frame, frame_heatmap
        print "End"