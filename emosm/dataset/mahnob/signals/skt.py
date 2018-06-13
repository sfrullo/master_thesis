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

        fps = self.metadata.info["sfreq"]

        # low-pass filter data
        dataf = data.copy()
        dataf.filter(l_freq=None, h_freq=1., fir_window="hann")

        # resample data to new fps
        # data.resample(new_fps)
        # dataf.resample(new_fps)

        y = data.get_data().flatten()
        yf = dataf.get_data().flatten()

        # Apply normalization
        yn = (y - y.mean()) / y.std()
        ynf = (yf - yf.mean()) / yf.std()

        ynfs, _ = biosppy.tools.smoother(signal=ynf, kernel='boxzen', size=int(0.75 * fps), mirror=True)

        # display the extracted EDA components
        if show:
            tm = np.arange(1., len(yn) + 1.)
            plt.plot(tm, yn, label='temp original')
            plt.plot(tm, ynf, label='temp filtered')
            plt.plot(tm, ynfs, label='temp filtered smoothed')
            plt.title('Skin Temperature')
            plt.legend(loc='best')
            plt.show()

        return ynfs

