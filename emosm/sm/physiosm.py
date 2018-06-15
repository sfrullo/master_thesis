    # coding: utf-8

# native

# external
import numpy as np
import matplotlib.pyplot as plt

# custom
import emosm.tools.utils as utils
import emosm.sm.basesm as basesm
import emosm.fe.feature_extractor as fe

import emosm.dataset.mahnob.config as config

class PhisioSaliencyMap(basesm.BaseSaliencyMap):
    """docstring for PhisioSaliencyMap"""
    def __init__(self, data, gaze, **opts):
        super(PhisioSaliencyMap, self).__init__()
        self.data = data
        self.gaze = gaze

        self.sigtype = opts["sigtype"]
        self.attribute = opts["attribute"]
        self.psyco_construct = opts["psyco_construct"]
        self.fps = opts["fps"]

    def compute_saliency_map(self, limit_frame=None, display_size=None):
        print "start compute saliency map"

        if display_size is None:
            raise ValueError("display_size must be a tuple")

        coordinates = self.gaze["coordinates"] / config.FRAME_SCALE_FACTOR
        len_coor = coordinates.shape[0]

        # compute features for each session
        features = None
        for d in self.data:
            data = d.get_data(preprocess=True, new_fps=self.fps)
            index, f = fe.extract(data, sigtype=self.sigtype, attribute=self.attribute, psyco_construct=self.psyco_construct, fps=self.fps)
            if features is None:
                features = np.array((f[:len_coor],))
            else:
                features = np.vstack([features, f[:len_coor]])

        # zip physiological data with proper gaze coordinate
        sm_data = np.concatenate([coordinates, features.T[:,:,np.newaxis]], axis=2)

        if limit_frame is not None:
            sm_data = sm_data[:limit_frame]

        print "Process frame"
        for frame_number, data in enumerate(sm_data):
            print "#{}".format(frame_number)
            frame_heatmap = self.compute_frame_saliency_map(data, display_size)
            yield frame_heatmap
        print "End"