# coding: UTF-8

import unittest

import numpy as np

from pyresemblance import threedlark
from pyresemblance import consts

from pyresemblance.utils import edge_mirror_3

import tests.utils
from tests.pyresemblance import testcase

class TestThreeDLARK(unittest.TestCase):

    def setUp(self):
        seq = tests.utils.load_gradient_mat('person01_boxing_d2_uncomp_64_64_40.mat')
        self.threeDLARK = threedlark.ThreeDLARK(seq=seq, w_size=3, w_size_t=3, smoothing=1.0, alpha=1)

    def test_compute_kernel(self):
        kernel = self.threeDLARK.compute_kernel(mask=consts.fspecial_disk_1)
        expected_result = testcase.test_threedlark_kernel_fspecial_disk_1
        np.testing.assert_allclose(kernel, expected_result, rtol=1e-7)

    def test_get_gradient(self):
        for tc in testcase.test_get_gradient:
            input_data, expected_result = tc.values()
            result = self.threeDLARK.get_gradient()
            np.testing.assert_array_equal(result, expected_result)

class TestEdgeMirror3(unittest.TestCase):

    def test_edge_mirror_3(self):
        for tc in testcase.test_edge_mirror_3:
            input_data, expected_result = tc.values()
            result = edge_mirror_3(input_data, width=((1,), (1,), (1,)))
            np.testing.assert_equal(result, expected_result)