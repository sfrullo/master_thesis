# coding: UTF-8

import unittest

import numpy as np

from emosm.pyresemblance import saliencymap

from emosm.tools import utils
from emosm.tools import matio

from tests.pyresemblance import testcase

class TestSaliencyMap(unittest.TestCase):

    def setUp(self):
        seq = matio.load_mat_file('person01_boxing_d2_uncomp_64_64_40.mat')
        self.spaceTimeSaliencyMap = saliencymap.SpaceTimeSaliencyMap(seq=seq)

    def test_compute_saliency_map(self):
        sm = self.spaceTimeSaliencyMap.compute_saliency_map()
        expected_result = matio.load_mat_file("SM.mat")
        sm = sm.flatten()
        er = expected_result.flatten()
        np.testing.assert_equal(sm.sort(), er.sort())