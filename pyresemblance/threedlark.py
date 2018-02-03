# coding: UTF-8

import numpy as np

import consts
import utils

class ThreeDLARK:
    """Compute 3-D LARK descriptors

    Attributes
    ----------
    arg : TYPE
        Description
    """

    def __init__(self, seq=None, w_size=3, w_size_t=3, smoothing=1.0, alpha=0.42, sigma=0.7):

        if seq is None:
            raise ValueError("Seq must be a valid sequence")

        self.seq = seq

        self.w_size = w_size
        self.w_size_t = w_size_t
        self.smoothing = smoothing
        self.alpha = alpha
        self.sigma = sigma

        self.win = (w_size-1)/2
        self.win_t = (w_size_t-1)/2

        lwin = np.linspace(-self.win, self.win, 3) # --> array([-1.,  0.,  1.])
        lwint = np.linspace(-self.win_t, self.win_t, 3)

        self.mask_x = np.tile(lwin, (3, 1))  # --> array([[-1.,  0.,  1.], [-1.,  0.,  1.], [-1.,  0.,  1.]])
        self.mask_y = np.tile(lwin, (3, 1))
        self.mask_t = np.tile(lwint, (3, 1))


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

        def get_covariances(self):

            kernel = self.compute_kernel(mask=consts.fspecial_disk_1)
            P = sum(kernel.flatten())

            M, N, T = self.seq.shape
            wsize = self.wsize

            lambda1 = 1
            lambda2 = 10**(-7)
            alpha = 8*10**(-3)

            # Init covariance matrices
            C11 = np.zeros([M,N,T])
            C12 = np.zeros([M,N,T])
            C13 = np.zeros([M,N,T])

            C22 = np.zeros([M,N,T])
            C23 = np.zeros([M,N,T]) # C21 = C12

            C33 = np.zeros([M,N,T]) # C13 = C31, C23 = C32

            width = (self.win, self.win, self.win_t)
            zx, zy, zt = [ utils.edge_mirror_3(g, width=width) for g in self.get_gradient() ]

            for i in xrange(0, M-1):
                for j in xrange(0, N-1):
                    for k in xrange(0, T-1):
                        gx, gy, gt = [ z[i:i+wsize, i:i+wsize, i:i+wsize] * kernel for z in (zx,zy,zt) ]

                        G = np.column_stack([ utils.to_column(g) for g in [ gx, gy, gt ] ]);

                        U, S, Vh = np.linalg.svd(G)

                        s = []
                        ds = np.diag(s)
                        s[0] = (ds[0] + lambda1) / (np.sqrt(ds[1],ds[2]) + lambda2)
                        s[1] = (ds[1] + lambda1) / (np.sqrt(ds[0],ds[2]) + lambda2)
                        s[2] = (ds[2] + lambda1) / (np.sqrt(ds[0],ds[1]) + lambda2)

                        gamma = ( ( s1*s2*s3 + lambda2 ) / P ) ** alpha

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

            self.C11 = utils.edge_mirror_3(C11,width=width)
            self.C12 = utils.edge_mirror_3(C12,width=width)
            self.C22 = utils.edge_mirror_3(C22,width=width)
            self.C23 = utils.edge_mirror_3(C23,width=width)
            self.C33 = utils.edge_mirror_3(C33,width=width)
            self.C13 = utils.edge_mirror_3(C13,width=width)