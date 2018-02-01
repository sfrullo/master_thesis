# coding: UTF-8

import unittest

import numpy as np

from pyresemblance import threedlark
from pyresemblance import consts

from pyresemblance.utils import edge_mirror_3

from tests.pyresemblance import test_case as test_case

class TestThreeDLARK(unittest.TestCase):

    def setUp(self):
        self.threeDLARK = threedlark.ThreeDLARK(w_size=3, w_size_t=3, smoothing=1.0, alpha=1)

    def test_compute_kernel(self):
        kernel = self.threeDLARK.compute_kernel(mask=consts.fspecial_disk_1)
        expected_result = test_case.test_threedlark_kernel_fspecial_disk_1
        np.testing.assert_allclose(kernel, expected_result, rtol=1e-7)


class TestEdgeMirror3(unittest.TestCase):

    def test_edge_mirror_3(self):
        for tc in test_case.test_edge_mirror_3:
            input_data, expected_result = tc.values()
            result = edge_mirror_3(input_data, width=((1,), (1,), (1,)))
            np.testing.assert_equal(result, expected_result)