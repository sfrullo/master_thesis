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


class BaseSaliencyMap(object):


    def compute_frame_saliency_map(self, data, display_size, mean_data=None, normalize=True):

        # mean data in case of multiple sessions
        if mean_data is not None:
            data = data.mean(axis=1)

        x0 = y0 = 0
        x1, y1 = display_size
        w, h = display_size

        heatmap = utils.grid_density_gaussian_filter(x0, y0, x1, y1, w, h, data)

        if normalize is True:
            heatmap *= 1/heatmap.max()

        return heatmap

    def compute_saliency_map(self):
        raise NotImplementedError("compute_saliency_map must be implemented")
