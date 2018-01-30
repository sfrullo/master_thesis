# coding: UTF-8

import unittest

import numpy as np

from pyresemblance import threedlark
from pyresemblance import consts

class TestStringMethods(unittest.TestCase):

    def setUp(self):
    	self.threeDLARK = threedlark.ThreeDLARK(w_size=3, w_size_t=3, smoothing=1.0, sensitiviy=1)

    @unittest.expectedFailure
    def test_compute_kernel(self):
    	kernel = self.threeDLARK.compute_kernel(wsize=3, mask=consts.fspecial_disk_1)
    	expected_result = np.array([[
		    [ 0.0023, 0.0788, 0.0023],
		    [ 0.0788, 1.0000, 0.0788],
		    [ 0.0023, 0.0788, 0.0023]],

		    [[ 0.0164, 0.2085, 0.0164],
		    [ 0.2085, 1.0000, 0.2085],
		    [ 0.0164, 0.2085, 0.0164]],

		    [[ 0.0023, 0.0788, 0.0023],
		    [ 0.0788, 1.0000, 0.0788],
		    [ 0.0023, 0.0788, 0.0023]]
		])
        self.assertEquals(kernel, expected_result)