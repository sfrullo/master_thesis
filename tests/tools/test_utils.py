# coding: UTF-8

import unittest

import numpy as np

from emosm.tools import utils

class TestUtils(unittest.TestCase):

    def test_moving_window_data_per_frame_generator_one_subject(self):

        input_data = np.array(range(30)).reshape((10,1,3))
        expected_result = [
            [[0, 1, 2],
             [3, 4, 5],
             [6, 7, 8]
            ],

            [[ 3,  4,  5],
             [ 6,  7,  8],
             [ 9, 10, 11],
             [12, 13, 14],
             [15, 16, 17]
            ],

            [[12, 13, 14],
             [15, 16, 17],
             [18, 19, 20],
             [21, 22, 23],
             [24, 25, 26]
            ],

            [[21, 22, 23],
             [24, 25, 26],
             [27, 28, 29]
            ]
        ]

        result = list(utils.moving_window_data_per_frame_generator(input_data, spf=3, ws=2))
        np.testing.assert_equal(expected_result, result)

    # @unittest.skip
    def test_moving_window_data_per_frame_generator_multiple_subject(self):

        input_data = np.array(range(90)).reshape((10,3,3))
        expected_result = [
            [[ 0,  1,  2], [ 3,  4,  5], [ 6,  7,  8],
             [ 9, 10, 11], [12, 13, 14], [15, 16, 17],
             [18, 19, 20], [21, 22, 23], [24, 25, 26]
            ],

            [[ 9, 10, 11], [12, 13, 14], [15, 16, 17],
             [18, 19, 20], [21, 22, 23], [24, 25, 26],
             [27, 28, 29], [30, 31, 32], [33, 34, 35],
             [36, 37, 38], [39, 40, 41], [42, 43, 44],
             [45, 46, 47], [48, 49, 50], [51, 52, 53]
            ],

            [[36, 37, 38], [39, 40, 41], [42, 43, 44],
             [45, 46, 47], [48, 49, 50], [51, 52, 53],
             [54, 55, 56], [57, 58, 59], [60, 61, 62],
             [63, 64, 65], [66, 67, 68], [69, 70, 71],
             [72, 73, 74], [75, 76, 77], [78, 79, 80]
            ],

            [[63, 64, 65], [66, 67, 68], [69, 70, 71],
             [72, 73, 74], [75, 76, 77], [78, 79, 80],
             [81, 82, 83], [84, 85, 86], [87, 88, 89]
            ]
        ]

        result = list(utils.moving_window_data_per_frame_generator(input_data, spf=3, ws=2))

        print result

        np.testing.assert_equal(expected_result, result)