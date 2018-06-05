# coding: utf-8

# native

# external
import mne
import numpy as np
import matplotlib.pyplot as plt

# custom
import emosm.tools.utils as utils
import emosm.dataset.mahnob.config as config

import emosm.tools.cvxEDA as cvxEDA

from emosm.dataset.mahnob.signals import physio

class EDAData(physio.PhysioBase):

    """docstring for GazeData"""
    def __init__(self, filename):
        super(EDAData, self).__init__(filename=filename)
        self.load_data()

    def load_data(self):
        print 'Load GSR data..'

        fps = self.metadata.info["sfreq"]
        tstart = self.metadata.times[self.start]
        tstop = self.metadata.times[int(self.stop + 10 * fps)]

        self.raw_data = self.metadata.load_data().pick_channels(['GSR1']).crop(tstart, tstop)

    def get_data(self, preprocess=False, **kwargs):
        # Load GSR data from start point
        data = self.raw_data.copy()

        if preprocess:
            data = self.preprocess(data, **kwargs)
            return data

        return data.get_data(0).flatten()

    def preprocess(self, data, new_fps=25, show=False):

        print "prepocess data ..."

        # low-pass filter data
        data.filter(l_freq=None, h_freq=5)

        # resample data
        data.resample(new_fps)

        y = data.get_data().flatten()

        # Apply normalization
        yn = (y - y.mean()) / y.std()

        # compute convex optimization from (https://github.com/lciti/cvxEDA)
        # to extract phasic component
        [r, p, t, l, d, e, obj] = cvxEDA.cvxEDA(yn, 1. / new_fps, options={'show_progress':False})

        # display the extracted EDA components
        if show:
            tm = np.arange(1., len(yn) + 1.)
            plt.plot(tm, yn, label='EDA')
            plt.plot(tm, r, label='Phasic')
            plt.plot(tm, t, label='Tonic')
            plt.title('EDA decomposition')
            plt.legend(loc='best')
            plt.show()

        return r

