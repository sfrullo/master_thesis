# coding: utf-8

# native

# external
import numpy as np

# custom
import emosm.tools.utils as utils

import emosm.dataset.mahnob.config as config

class GazeData(object):

    """docstring for GazeData"""
    def __init__(self, filename):
        super(GazeData, self).__init__()
        self.filename = filename

        self.__load_gaze_from_file()

    def __load_gaze_from_file(self):
        print 'Load gaze file.'

        with open(self.filename, 'r') as f:
            # skip 24 lines
            for i in range(1,config.HEADER_LENGTH): f.readline()

            header = f.readline().replace('\n', '').rstrip().split('\t')

            lines = f.readlines()
            start = [ i for i,l in enumerate(lines) if "MovieStart" in l ][0] + 1
            end = [ i for i,l in enumerate(lines) if "MovieEnd" in l ][0]

            line = lines[start-1].replace('\n', '').rstrip().split('\t')
            stimuli_name = dict(zip(header, self.cast_entry_values(line)))["Descriptor"]

            data = []
            for line in lines[start:end]:
                d = line.replace('\n', '').rstrip().split('\t')
                data_entry = dict(zip(header, self.cast_entry_values(d)))

                if data_entry.get("StimuliName") and data_entry.get("StimuliName") == stimuli_name:
                    data.append(data_entry)

        self.header = header
        self.data = data
        self.startIndex = start
        self.endIndex = end

    def cast_entry_values(self, entry):
        new_entry = []
        for value in entry:
            try:
                new_entry.append(int(value))
            except ValueError:
                try:
                    new_entry.append(float(value))
                except ValueError:
                    new_entry.append(value)
        return new_entry

    def _remove_blinks(self, data):
        """ Remove blinks interpolating the last and the first valid values
            ref: https://stackoverflow.com/questions/6518811/interpolate-nan-values-in-a-numpy-array
        """
        nans = np.isnan(data)
        if np.any(nans):
            x = lambda a: a.nonzero()[0]
            data[nans] = np.interp(x(nans), x(~nans), data[~nans])
        return data

    def _extract_data_from_key(self, key, preprocess=False):
        """ Extract data using key, filter invalid values and, eventually, remove blinks """
        data = np.array([ d[key] if not isinstance(d[key], str) and d[key] >= 0 else np.nan for d in self.data ])
        if preprocess:
            data = self._remove_blinks(data=data)
            data = utils.resample(data, config.EYE_TRACKING_SAMPLE_RATE, config.MEDIA_FPS)
        return data

    def get_gaze_coordinates(self, mapped=False, preprocess=False):
        keys = ("GazePointX", "GazePointY")
        if mapped:
            keys = ("MappedGazeDataPointX", "MappedGazeDataPointY")

        X = self._extract_data_from_key(key=keys[0], preprocess=preprocess)
        Y = self._extract_data_from_key(key=keys[1], preprocess=preprocess)

        coordinates = np.array(zip(X, Y), dtype=np.float32)

        return coordinates

    def get_fixations_coordinates(self, preprocess=False):
        keys = ("MappedFixationPointX", "MappedFixationPointY")

        X = self._extract_data_from_key(key=keys[0], preprocess=preprocess)
        Y = self._extract_data_from_key(key=keys[1], preprocess=preprocess)

        coordinates = np.array(zip(X, Y), dtype=np.float32)

        return coordinates

    def get_fixations_duration(self, preprocess=False):
        key = "FixationDuration"

        D = self._extract_data_from_key(key=key, preprocess=preprocess)

        durations = np.array(D, dtype=np.float32)

        return durations

    def get_fixations_data(self, preprocess=False):
        coordinates = self.get_fixations_coordinates(preprocess=preprocess)
        durations = self.get_fixations_duration(preprocess=preprocess)

        fixation_data = np.append(coordinates, utils.to_column(durations), axis=1)

        return fixation_data

