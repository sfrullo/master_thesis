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
        coordinates = self.gaze["fixations"][:,:,0:2]
        len_coor = coordinates.shape[0]

        # zip physiological data with proper gaze coordinate
        sm_data = np.concatenate([coordinates, self.physio[:len_coor,:,np.newaxis]], axis=2)

        if limit_frame is not None:
            sm_data = sm_data[:limit_frame]

        print "Process frame"
        frame_heatmap_list = []
        for frame_number, data in enumerate(sm_data):
            print "# {}/{}".format(frame_number, sm_data.shape[0])
            frame_heatmap = self.compute_frame_saliency_map(data, display_size)
            # yield frame_heatmap
            frame_heatmap_list.append(frame_heatmap)
        print "End"

        frame_heatmap_list = np.asarray(frame_heatmap_list)

        # frame_heatmap_list *= 1/frame_heatmap_list.max()
        frame_heatmap_list = (frame_heatmap_list - frame_heatmap_list.mean())/frame_heatmap_list.max()

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