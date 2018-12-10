    # coding: utf-8

# native
import itertools

# external
import numpy as np
import matplotlib.pyplot as plt

# custom
import emosm.tools.utils as utils
import emosm.sm.basesm as basesm

import emosm.dataset.mahnob.config as config

class PhysioSaliencyMap(basesm.BaseSaliencyMap):
    """docstring for PhysioSaliencyMap"""
    def __init__(self, physio, gaze, **kwargs):
        super(PhysioSaliencyMap, self).__init__()
        self.physio = physio
        self.gaze = gaze

    def compute_saliency_map(self, limit_frame=None, display_size=None):
        print "start compute saliency map"

        if display_size is None:
            raise ValueError("display_size must be a tuple")

        # keep only fixations
        coordinates = self.gaze['coordinates']
        physio = self.physio
        len_coor = coordinates.shape[0]

        if limit_frame is not None:
            coordinates = coordinates[:limit_frame]
            physio = physio[:limit_frame]

        print coordinates.squeeze()
        print physio

        # zip physiological data with proper gaze coordinate
        sm_data = np.append(coordinates.squeeze(), physio, axis=1)

        print sm_data.shape

        print "Process frame"
        frame_heatmap_list = []
        for frame_number, data in enumerate(sm_data):
            print "# {}/{}".format(frame_number, sm_data.shape[0])
            frame_heatmap = self.compute_frame_saliency_map(data, display_size)
            # yield frame_heatmap
            frame_heatmap_list.append(frame_heatmap)
        print "End"

        X = np.asarray(frame_heatmap_list)
        X_std = (X - X.min()) / (X.max() - X.min())
        frame_heatmap_list = X_std * (1 - 0) + 0

        return frame_heatmap_list


##
## SALIENCY MAP COMPOSER
##

def physioSaliencyMapComposer(saliency_map_list, rules={}):
    """Generator that yield composed saliencymap for given a set of Physiological SM, following given rules of composition"""
    for sm in itertools.izip(*saliency_map_list):
        x = np.array(sm)
        mixed_sm = np.sum(x, axis=0)
        mixed_sm *= 1/mixed_sm.max()
        yield mixed_sm