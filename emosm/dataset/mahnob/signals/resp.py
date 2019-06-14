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

        y = data.get_data().flatten()

        # extract respiration features
        ts, filtered, zeros, resp_rate_ts, resp_rate = biosppy.signals.resp.resp(signal=y, sampling_rate=fps, show=show)

        # resample
        filtered = utils.resample(filtered, fps, new_fps)

        # Apply normalization
        # filtered = utils.normalize(filtered)

        return filtered

