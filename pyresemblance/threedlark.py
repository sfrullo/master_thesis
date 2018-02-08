# coding: UTF-8

import logging

import numpy as np

import consts

from tools import utils

class ThreeDLARK:
    """Compute 3-D LARK descriptors

    Attributes
    ----------
    arg : TYPE
        Description
    """

    def __init__(self, seq=None, w_size=3, w_size_t=3, smoothing=1.0):

        if seq is None:
            raise ValueError("Seq must be a valid sequence")

        self.seq = seq

        self.w_size = w_size
        self.w_size_t = w_size_t
        self.smoothing = smoothing

        self.win = (w_size-1)/2
        self.win_t = (w_size_t-1)/2

    def get_gradient(self):
        zy, zx, zt = np.gradient(self.seq)
        return [zx, zy, zt]

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

        w_size = self.w_size_t
        win = self.win

        kernel = np.zeros([w_size, w_size, w_size])

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

    def get_covariance(self, shape=None):
        logging.info("S - get_covariance")

        if shape is None:
            shape = self.seq.shape

        kernel = self.compute_kernel(mask=consts.fspecial_disk_1)
        P = sum(kernel.flatten())

        w_size = self.w_size
        w_size_t = self.w_size_t

        lambda1 = 1
        lambda2 = 10**(-7)
        alpha = 8*10**(-3)

        # Init covariance matrices
        C11 = np.zeros(shape)
        C12 = np.zeros(shape)
        C13 = np.zeros(shape)

        C22 = np.zeros(shape)
        C23 = np.zeros(shape) # C21 = C12

        C33 = np.zeros(shape) # C13 = C31, C23 = C32

        width = ((self.win,), (self.win,), (self.win_t,),) # ((1,), (1,), (1,))
        zx, zy, zt = [ utils.edge_mirror_3(g, width=width) for g in self.get_gradient() ]

        for i in xrange(shape[0]):
            for j in xrange(shape[1]):
                for k in xrange(shape[2]):
                    gx, gy, gt = [ z[i:i+w_size, j:j+w_size, k:k+w_size_t] * kernel for z in (zx,zy,zt) ]

                    G = np.column_stack([ utils.to_column(g) for g in [ gx, gy, gt ] ]);

                    U, S, Vh = np.linalg.svd(G, full_matrices=False)

                    s = []
                    s += [ (S[0] + lambda1) / (np.sqrt(S[1]*S[2]) + lambda1) ]
                    s += [ (S[1] + lambda1) / (np.sqrt(S[0]*S[2]) + lambda1) ]
                    s += [ (S[2] + lambda1) / (np.sqrt(S[0]*S[1]) + lambda1) ]

                    gamma = ( ( s[0]*s[1]*s[2] + lambda2 ) / P ) ** alpha

                    tmp = s[0] * Vh[:,0].reshape(3,1).dot(Vh[:,0].reshape(3,1).transpose()) \
                        + s[1] * Vh[:,1].reshape(3,1).dot(Vh[:,1].reshape(3,1).transpose()) \
                        + s[2] * Vh[:,2].reshape(3,1).dot(Vh[:,2].reshape(3,1).transpose())

                    tmp = tmp * gamma

                    C11[i,j,k] = tmp[0,0]
                    C12[i,j,k] = tmp[0,1]
                    C13[i,j,k] = tmp[0,2]
                    C22[i,j,k] = tmp[1,1]
                    C23[i,j,k] = tmp[1,2]
                    C33[i,j,k] = tmp[2,2]

        C11 = utils.edge_mirror_3(C11,width=width)
        C12 = utils.edge_mirror_3(C12,width=width)
        C22 = utils.edge_mirror_3(C22,width=width)
        C23 = utils.edge_mirror_3(C23,width=width)
        C33 = utils.edge_mirror_3(C33,width=width)
        C13 = utils.edge_mirror_3(C13,width=width)

        logging.info("E - get_covariance")

        return [ C11, C12, C22, C23, C33, C13 ]

    def get_lark(self):

        shape = self.seq.shape

        x3, x2, x1 = np.mgrid[-self.win:self.win+1, -self.win:self.win+1, -self.win_t:self.win_t+1]

        x11 = x1**2
        x12 = 2*x1*x2
        x13 = 2*x1*x3

        x22 = x2**2
        x23 = 2*x2*x3

        x33 = x3**2

        shape = list(self.seq.shape) + [self.w_size, self.w_size, self.w_size_t]

        x1x1 = x11.reshape([1, x11.size]).repeat(self.seq.size,0).reshape(shape)
        x1x2 = x12.reshape([1, x12.size]).repeat(self.seq.size,0).reshape(shape)
        x1x3 = x13.reshape([1, x13.size]).repeat(self.seq.size,0).reshape(shape)
        x2x2 = x22.reshape([1, x22.size]).repeat(self.seq.size,0).reshape(shape)
        x2x3 = x23.reshape([1, x23.size]).repeat(self.seq.size,0).reshape(shape)
        x3x3 = x33.reshape([1, x33.size]).repeat(self.seq.size,0).reshape(shape)

        C11, C12, C22, C23, C33, C13 = self.get_covariance()

        # Geodesic distance computation between a center and surrounding voxels
        lark = np.zeros(shape)
        for i in range(self.w_size):
            for j in range(self.w_size):
                for k in range(self.w_size_t):
                    v = C11[ i:i+shape[0], j:j+shape[1], k:k+shape[2] ]*x1x1[:,:,:,i,j,k] \
                      + C22[ i:i+shape[0], j:j+shape[1], k:k+shape[2] ]*x2x2[:,:,:,i,j,k] \
                      + C33[ i:i+shape[0], j:j+shape[1], k:k+shape[2] ]*x3x3[:,:,:,i,j,k] \
                      + C12[ i:i+shape[0], j:j+shape[1], k:k+shape[2] ]*x1x2[:,:,:,i,j,k] \
                      + C13[ i:i+shape[0], j:j+shape[1], k:k+shape[2] ]*x1x3[:,:,:,i,j,k] \
                      + C23[ i:i+shape[0], j:j+shape[1], k:k+shape[2] ]*x2x3[:,:,:,i,j,k]

                    lark[:,:,:,i,j,k] = v

        # Convert geodesic distance to self-similarity
        lark = np.exp(-lark * 0.5 / self.smoothing**2);

        shape = list(self.seq.shape) + [ self.w_size * self.w_size * self.w_size_t ]
        lark = np.reshape(lark, shape);

        return lark
