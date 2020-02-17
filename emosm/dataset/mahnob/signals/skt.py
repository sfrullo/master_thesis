# coding: utf-8

# native

# external
import mne
import numpy as np
import matplotlib.pyplot as plt
import biosppy

from scipy import interpolate

# custom
import emosm.tools.utils as utils
import emosm.dataset.mahnob.config as config

from emosm.dataset.mahnob.signals import physio

class SKTData(physio.PhysioBase):

    """docstring for SKTData"""
    def __init__(self, filename):
        super(SKTData, self).__init__(filename=filename)
        self.load_data()

    def load_data(self):
        print 'Load respiration data..'

        fps = self.metadata.info["sfreq"]
        tstart = self.metadata.times[self.start]
        tstop = self.metadata.times[int(self.stop + 10 * fps)]

        self.raw_data = self.metadata.load_data().pick_channels(['Temp']).crop(tstart, tstop)

    def preprocess(self, data, new_fps=25, show=False):

        print "prepocess data ..."

        fo = 2 # filter order
        fc = 1 # filter cut frequency
        ft = 'lowpass' # filter type

        fps = self.metadata.info["sfreq"]

        y = data.get_data().flatten()

        # Filtering
        filtered, _, _ = biosppy.tools.filter_signal(signal=y,
                                     ftype='butter',
                                     band='lowpass',
                                     order=fo,
                                     frequency=fc,
                                     sampling_rate=fps)

        skt = utils.resample(filtered, fps, new_fps)

        # display the extracted EDA components
        if show:
            tm = np.arange(1., len(y) + 1.)
            plt.plot(tm, y, label='temp original')
            plt.plot(tm, filtered, label='temp filtered')
            plt.title('Skin Temperature')
            plt.legend(loc='best')
            plt.show()

        # Apply normalization
        # skt = utils.normalize(skt)

        return skt

