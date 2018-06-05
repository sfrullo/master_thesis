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

class RespData(physio.PhysioBase):

    """docstring for RespData"""
    def __init__(self, filename):
        super(RespData, self).__init__(filename=filename)
        self.load_data()

    def load_data(self):
        print 'Load respiration data..'

        fps = self.metadata.info["sfreq"]
        tstart = self.metadata.times[self.start]
        tstop = self.metadata.times[int(self.stop + 10 * fps)]

        self.raw_data = self.metadata.load_data().pick_channels(['Resp']).crop(tstart, tstop)

    def preprocess(self, data, new_fps=25, show=False):

        print "prepocess data ..."

        fps = self.metadata.info["sfreq"]

        # low-pass filter data
        data.filter(l_freq=None, h_freq=5)

        # resample data to new fps
        data.resample(new_fps)

        y = data.get_data().flatten()

        # Apply normalization
        yn = (y - y.mean()) / y.std()

        # extract respiration features
        ts, filtered, zeros, resp_rate_ts, resp_rate = biosppy.signals.resp.resp(signal=yn, sampling_rate=new_fps, show=show)

        # interpolate respiration rate to restore original length
        f = interpolate.interp1d(resp_rate_ts, resp_rate, bounds_error=False, fill_value="extrapolate")
        resp_rate = f(xrange(yn.size))

        return resp_rate

