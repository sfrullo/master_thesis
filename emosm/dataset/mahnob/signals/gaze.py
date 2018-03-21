# coding: utf-8

# native

# external
import numpy as np

# custom
import emosm.tools.utils as utils

HEADER_LENGTH = 24

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
            for i in range(1,HEADER_LENGTH): f.readline()

            header = f.readline().replace('\n', '').rstrip().split('\t')

            lines = f.readlines()
            start = [ i for i,l in enumerate(lines) if "MovieStart" in l ][0] + 1
            end = [ i for i,l in enumerate(lines) if "MovieEnd" in l ][0]

            data = []
            for line in lines[start:end]:
                d = line.replace('\n', '').rstrip().split('\t')
                data_entry = dict(zip(header, self.cast_entry_values(d)))
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

    def _extract_data_from_key(self, key):
        data = [ d[key] if not isinstance(d[key], str) else 0 for d in self.data ]
        return data

    def get_gaze_coordinates(self, mapped=False):
        keys = ("GazePointX", "GazePointY")
        if mapped:
            keys = ("MappedGazeDataPointX", "MappedGazeDataPointY")

        X = self._extract_data_from_key(keys[0])
        Y = self._extract_data_from_key(keys[1])

        coordinates = np.array(zip(X, Y), dtype=np.float32)

        return coordinates

    def get_fixations_coordinates(self):
        keys = ("MappedFixationPointX", "MappedFixationPointY")

        X = self._extract_data_from_key(keys[0])
        Y = self._extract_data_from_key(keys[1])

        coordinates = np.array(zip(X, Y), dtype=np.float32)

        return coordinates

    def get_fixations_duration(self):
        keys = ("FixationDuration")

        D = self._extract_data_from_key(key="FixationDuration")

        durations = np.array(D, dtype=np.float32)

        return durations

    def get_fixations_data(self):
        coordinates = self.get_fixations_coordinates()
        durations = self.get_fixations_duration()

        fixation_data = np.append(coordinates, utils.to_column(durations), axis=1)

        return fixation_data

