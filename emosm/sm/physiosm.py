    # coding: utf-8

# native

# external
import numpy as np
import matplotlib.pyplot as plt

# custom
import emosm.tools.utils as utils
import emosm.fe.feature_extractor as fe

import emosm.dataset.mahnob.config as config

class PhisioSaliencyMap(object):
    """docstring for PhisioSaliencyMap"""
    def __init__(self, data, gaze, media, **opts):
        super(PhisioSaliencyMap, self).__init__()
        self.data = data
        self.gaze = gaze
        self.media = media

        self.sigtype = opts["sigtype"]
        self.attribute = opts["attribute"]
        self.psyco_construct = opts["psyco_construct"]
        self.fps = opts["fps"]


    def __compute_frame_saliency_map(self, data, display_size, normalize=True):

        # mean fixations in case of multiple sessions
        # if mean_data is None:
        #     X, Y, D = fixations.T
        # else:
        #     X, Y, D = fixations.mean(axis=0)

        x0 = y0 = 0
        x1, y1 = display_size
        w, h = display_size

        heatmap = utils.grid_density_gaussian_filter(x0, y0, x1, y1, w, h, data)

        if normalize is True:
            heatmap *= 1/heatmap.max()

        return heatmap

    def compute_saliency_map(self, limit_frame=None):
        print "start compute saliency map"

        coordinates = self.gaze["coordinates"] / config.FRAME_SCALE_FACTOR
        len_coor = coordinates.shape[0]

        # compute features for each session
        features = None
        for d in self.data:
            data = d.get_data(preprocess=True, new_fps=self.fps)
            index, f = fe.extract(data, sigtype=self.sigtype, attribute=self.attribute, psyco_construct=self.psyco_construct, fps=self.fps)
            if features is None:
                features = f[:len_coor]
            else:
                features = np.vstack([features, f[:len_coor]])

        # zip physiological data with proper gaze coordinate
        sm_data = np.concatenate([coordinates, features.T[:,:,np.newaxis]], axis=2)

        if limit_frame is not None:
            sm_data = sm_data[:limit_frame]

        scale_media = config.SCALE_MEDIA
        display_size = self.media.get_size(scaled=scale_media)
        media_frame = self.media.get_frames(limit_frame=limit_frame, scale=scale_media)

        print "Process frame"
        for frame_number, (data, frame) in enumerate(zip(sm_data, media_frame)):
            print "#{}".format(frame_number)
            frame_heatmap = self.__compute_frame_saliency_map(data, display_size)
            yield frame, frame_heatmap
        print "End"