# coding: UTF-8

import numpy as np

import consts

class ThreeDLARK:
	"""Compute 3-D LARK descriptors

	Attributes
	----------
	arg : TYPE
	    Description
	"""

	def __init__(self, w_size=None, w_size_t=None, smoothing=1.0, sensitiviy=None):

		self.w_size = w_size
		self.w_size_t = w_size_t
		self.smoothing = smoothing
		self.sensitiviy = sensitiviy

		self.win = (w_size-1)/2
		self.win_t = (w_size_t-1)/2

		lwin = np.linspace(-self.win, self.win, 3) # --> array([-1.,  0.,  1.])
		lwint = np.linspace(-self.win_t, self.win_t, 3)

 		self.mask_x = np.tile(lwin, (3, 1))  # --> array([[-1.,  0.,  1.], [-1.,  0.,  1.], [-1.,  0.,  1.]])
 		self.mask_y = np.tile(lwin, (3, 1))
		self.mask_t = np.tile(lwint, (3, 1))

		self.kernel = self.compute_kernel(wsize=w_size_t, mask=consts.fspecial_disk_1)
		# for i in range(0, self.w_size_t - 1)

	def compute_kernel(self, wsize=None, mask=None):
		"""Summary

		Parameters
		----------
		wsize : None, optional
		    Description
		mask : None, optional
		    Description

		Raises
		------
		ValueError
		    Description
		"""
		if wsize is None:
			raise ValueError("Must give an window size")

		if mask is None:
			raise ValueError("Must give an initial mask value")

		kernel = np.zeros([wsize, wsize, wsize])
		return kernel