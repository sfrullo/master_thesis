# coding: utf-8

# native

# external
import mne
import numpy as np

# custom
import emosm.tools.utils as utils

import emosm.dataset.mahnob.config as config

class PhysioBase(object):

    raw_metadata = {}

    def __init__(self, filename):
        super(PhysioBase, self).__init__()
        self.filename = filename

        self.raw_data = None
        self.prepocessed_data = None

        self.__load_physiological_data_from_file()

    def __load_physiological_data_from_file(self):
        print 'Load data from {}..'.format(self.filename)

        if self.filename not in PhysioBase.raw_metadata:
            metadata = mne.io.read_raw_edf(self.filename)

            # find begin and end of stimulation
            status = metadata.copy().load_data().pick_channels(['STI 014']).get_data(0).flatten()
            status *= 1/np.max(status)
            status = np.diff(status)
            start, stop = np.where(status == 1)[0]

            raw_metadata = {}
            raw_metadata["metadata"] = metadata
            raw_metadata["start"] = start
            raw_metadata["stop"] = stop

            PhysioBase.raw_metadata[self.filename] = raw_metadata

        raw_metadata = PhysioBase.raw_metadata[self.filename]
        self.metadata = raw_metadata["metadata"].copy()
        self.start = raw_metadata["start"]
        self.stop = raw_metadata["stop"]

    def plot(self, original=False):
        data = self.raw_data if original else self.prepocessed_data
        plt.plot(data)
        plt.show()
