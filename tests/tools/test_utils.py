# coding: UTF-8

import unittest

import numpy as np

from emosm.tools import utils

class TestUtils(unittest.TestCase):

    def test_moving_window_data_per_frame_generator(self):
        input_data = np.array(range(30)).reshape((10,1,3))
        expected_result = np.array([
            np.array([[0, 1, 2],
                   [3, 4, 5],
                   [6, 7, 8]]),
            np.array([[ 3,  4,  5],
                   [ 6,  7,  8],
                   [ 9, 10, 11],
                   [12, 13, 14],
                   [15, 16, 17]]),
            np.array([[12, 13, 14],
                   [15, 16, 17],
                   [18, 19, 20],
                   [21, 22, 23],
                   [24, 25, 26]]),
            np.array([[21, 22, 23],
                   [24, 25, 26],
                   [27, 28, 29]]),
        ])



        result = list(utils.moving_window_data_per_frame_generator(input_data, spf=3, ws=2))

        print expected_result
        print result

        np.testing.assert_equal(expected_result, result)