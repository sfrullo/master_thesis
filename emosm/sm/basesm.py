# coding: utf-8

# native
import os
import os.path as path

# external
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as ndi

# custom
import emosm.tools.utils as utils
import emosm.dataset.mahnob.config as config


class BaseSaliencyMap(object):


    def compute_frame_saliency_map(self, data, display_size, mean_data=None, normalize=False):

        # mean data in case of multiple sessions
        if mean_data is not None:
            data = data.mean(axis=1)

        x0 = y0 = 0
        x1, y1 = display_size

        w, h = display_size

        x, y, d = data.T
        bins = (range(w), range(h))
        heatmap, xedges, yedges = np.histogram2d(x, y, bins=bins, weights=d, normed=normalize)
        heatmap = ndi.gaussian_filter(heatmap, sigma=8)

        return heatmap.T

    def compute_saliency_map(self):
        raise NotImplementedError("compute_saliency_map must be implemented")