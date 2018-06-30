# coding: utf-8
import logging

import sys, os
sys.path.append(os.path.dirname(__file__) + "/..")

import numpy as np

import threedlark
import consts

from PIL import Image

from tools import matio
from tools import utils

class SpaceTimeSaliencyMap(object):
    """docstring for SpaceTimeSaliencyMap"""
    def __init__(self, seq=None, w_size=3, w_size_t=3, sigma=0.7):

        seq = seq.astype(np.float)

        print seq.shape

        self.original_size = seq[0].shape[::-1]

        print self.original_size

        self.seq = []
        for f in seq:
            p = Image.fromarray(f)
            p = p.resize(size=(64,64), resample=Image.BILINEAR)
            self.seq.append(np.array(p))

        self.seq = np.array(self.seq)

        self.seq *= 1/self.seq.std()

        self.w_size = w_size
        self.w_size_t = w_size_t
        self.win = (w_size-1)/2
        self.win_t = (w_size_t-1)/2

        self.sigma = sigma

        self.threeDLARK = threedlark.ThreeDLARK(seq=self.seq, w_size=self.w_size, w_size_t=self.w_size_t)

    @utils.timeIt
    def compute_saliency_map(self):

        lark = self.threeDLARK.get_lark()

        # To avoid edge effect, we use mirror padding.
        s = lark.shape
        mirrored_lark = np.zeros([ s[0]+self.win*2, s[1]+self.win*2, s[2]+self.win_t*2, s[3] ])
        width = ((self.win,), (self.win,), (self.win_t,),) # ((1,), (1,), (1,))
        for i in range(lark.shape[3]):
            mirrored_lark[:,:,:,i] = utils.edge_mirror_3(lark[:,:,:,i], width=width)

        # Precompute Norm of center matrices and surrounding matrices
        norm_c = np.zeros(lark.shape[:-1])
        for i in range(lark.shape[0]):
            for j in range(lark.shape[1]):
                for k in range(lark.shape[2]):
                    norm_c[i,j,k] = np.linalg.norm(np.squeeze(lark[i,j,k,:]))

        norm_s = utils.edge_mirror_3(norm_c, width=width)

        shape_center = [ lark.shape[0] * lark.shape[1] * lark.shape[2], lark.shape[3]]
        center = lark.reshape(shape_center)

        shape_norm = [ lark.shape[0] * lark.shape[1] * lark.shape[2], 1]
        norm_c = norm_c.reshape(shape_norm)

        sm = np.zeros(norm_c.shape)
        for i in range(self.w_size):
            for j in range(self.w_size):
                for k in range(self.w_size_t):
                    # compute inner product between a center and surrounding matrices
                    wa = np.s_[ i:i+lark.shape[0], j:j+lark.shape[1], k:k+lark.shape[2], : ]
                    wb = np.s_[ i:i+lark.shape[0], j:j+lark.shape[1], k:k+lark.shape[2] ]
                    a = center * np.reshape(mirrored_lark[wa], shape_center)
                    b = norm_c * np.reshape(norm_s[wb], shape_norm)

                    # reshape a to columns and divide by b
                    v = utils.to_column(np.sum(a, axis=1)) / b

                    # compute self-resemblance using matrix cosine similarity
                    sm = sm + np.exp( ( -1 + v ) / self.sigma**2 )

        # Final saliency map values
        sm = 1 / sm
        sm = sm.reshape(lark.shape[:-1])

        sm_risize = []
        for f in sm:
            p = Image.fromarray(f)
            p = p.resize(size=self.original_size, resample=Image.BILINEAR)
            p = np.array(p)
            sm_risize.append(p)

        return np.array(sm_risize)


def main():

    seq = matio.load_mat_file('person01_boxing_d2_uncomp_64_64_40.mat')
    spaceTimeSaliencyMap = SpaceTimeSaliencyMap(seq=seq)
    sm = spaceTimeSaliencyMap.compute_saliency_map()

    print sm

if __name__ == '__main__':
    main()