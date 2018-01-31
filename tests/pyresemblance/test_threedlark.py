# coding: UTF-8

import unittest

import numpy as np

from pyresemblance import threedlark
from pyresemblance import consts

from tests.pyresemblance import consts as test_consts

class TestStringMethods(unittest.TestCase):

    def setUp(self):
    	self.threeDLARK = threedlark.ThreeDLARK(w_size=3, w_size_t=3, smoothing=1.0, sensitiviy=1)

    def test_compute_kernel(self):
    	kernel = self.threeDLARK.compute_kernel(mask=consts.fspecial_disk_1)
    	expected_result = test_consts.threedlark_kernel_fspecial_disk_1
        np.testing.assert_allclose(kernel, expected_result, rtol=1e-7)