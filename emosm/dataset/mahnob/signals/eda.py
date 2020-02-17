# coding: utf-8

# native

# external
import mne
import numpy as np
import matplotlib.pyplot as plt
import biosppy

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

    def preprocess(self, data, new_fps=25, show=False):

        print "prepocess data ..."

        fps = self.metadata.info['sfreq']
        y = data.get_data().flatten()

        # Filtering
        filtered, _, _ = biosppy.tools.filter_signal(signal=y,
                                     ftype='butter',
                                     band='lowpass',
                                     order=4,
                                     frequency=5,
                                     sampling_rate=fps)

        # Smoothing
        filtered, _ = biosppy.tools.smoother(signal=filtered,
                                  kernel='boxzen',
                                  size=int(0.75 * fps),
                                  mirror=True)

        # resample data
        y = utils.resample(filtered, fps, new_fps)

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

        # r = utils.normalize(r)

        return r

