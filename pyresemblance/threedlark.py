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

        self.kernel = self.compute_kernel(mask=consts.fspecial_disk_1)

    def compute_kernel(self, mask=None):
        """Summary

        Parameters
        ----------
        mask : None, optional
            Description

        Returns
        -------
        TYPE
            Description
        """
        if mask is None:
            raise ValueError("Must give an initial mask value")

        wsize = self.w_size_t
        win = self.win

        kernel = np.zeros([wsize, wsize, wsize])

        for i in range(np.size(kernel, 2)):
            kernel[i] = mask

        kernel = np.swapaxes(kernel, 0, 2)

        for i in range(np.size(kernel, 2)):
            kernel[i] *= mask

        kernel = np.swapaxes(kernel, 0, 1)

        for i in range(np.size(kernel, 2)):
            kernel[i] *= mask

        kernel = np.swapaxes(kernel, 0, 1)

        for i in range(np.size(kernel, 2)):
            kernel[i] = kernel[i]/kernel[i][win,win]

        return kernel