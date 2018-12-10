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

class ECGData(physio.PhysioBase):

    """docstring for ECGData"""
    def __init__(self, filename):
        super(ECGData, self).__init__(filename=filename)
        self.load_data()

    def load_data(self):
        print 'Load ECG data..'

        fps = self.metadata.info["sfreq"]
        tstart = self.metadata.times[self.start]
        tstop = self.metadata.times[int(self.stop + 10 * fps)]

        self.raw_data = self.metadata.load_data().pick_channels(['EXG1', 'EXG2', 'EXG3']).crop(tstart, tstop)

    def preprocess(self, data, new_fps=25, show=False):

        print "prepocess data ..."

        fps = self.metadata.info['sfreq']

        # ecg1 = data.get_data()[0]
        ecg2 = data.get_data()[1].flatten()
        # ecg3 = data.get_data()[2]

        # Extract Heart Rate values
        # results = biosppy.signals.ecg.ecg(ecg1, sampling_rate=fps, show=True)
        results = biosppy.signals.ecg.ecg(ecg2, sampling_rate=fps, show=show)
        # results = biosppy.signals.ecg.ecg(ecg3, sampling_rate=fps, show=True)

        t_raw = results[0]
        t_hr  = results[5]
        hr    = results[6]

        # Interpolate HR values to bring signal back to original size
        f = interpolate.interp1d(t_hr, hr, bounds_error=False, fill_value="extrapolate")
        tmp_HR = f(t_raw)

        tmp_HR = utils.resample(tmp_HR, fps, new_fps)

        tmp_HR = utils.normalize(tmp_HR)

        return tmp_HR