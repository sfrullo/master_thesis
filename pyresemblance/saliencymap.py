import numpy as np

import threedlark
import consts
import utils

class SpaceTimeSaliencyMap(object):
    """docstring for SpaceTimeSaliencyMap"""
    def __init__(self, seq=None, w_size=3, w_size_t=3, sigma=0.7):

        self.seq = seq

        self.w_size = w_size
        self.w_size_t = w_size_t
        self.win = (w_size-1)/2
        self.win_t = (w_size_t-1)/2

        self.sigma = sigma

        self.threeDLARK = threedlark.ThreeDLARK(seq=self.seq, w_size=self.w_size, w_size_t=self.w_size_t)

    def compute_saliency_map(self):

        lark = self.threeDLARK.get_lark()

        # To avoid edge effect, we use mirror padding.
        width = [self.win, self.win, self.win_t]
        for i in range(lark.shape[3]):
            mirrored_lark[:,:,:,i] = utils.edge_mirror_3(lark[:,:,:,i], width=width)

        # Precompute Norm of center matrices and surrounding matrices
        norm_c = np.zeros(lark.shape[:-1])
        for i in range(lark.shape[0]):
            for j in range(lark.shape[1]):
                for k in range(lark.shape[2]):
                    norm_c[i,j,k] = numpy.linalg.norm(np.squeeze(lark[i,j,k,:]))

        norm_s = utils.edge_mirror_3(norm_C, width=width)

        shape_center = [ lark.shape[0] * lark.shape[1] * lark.shape[2], lark.shape[3]]
        center = lark.reshape(shape_center)

        shape_norm = [ lark.shape[0] * lark.shape[1] * lark.shape[2], 1]
        norm_c = norm_c.reshape(shape_norm)

        sm = np.zeros(norm_c.shape)
        for i in range(self.w_size):
            for j in range(self.w_size):
                for k in range(self.w_size_t):
                    # compute inner product between a center and surrounding matrices
                    w = np.s_[ (i,i+lark.shape[0]), (j,j+lark.shape[1]), (l,l+lark.shape[2]), : ]
                    a = center * reshape(mirrored_lark([w]), shape_center)
                    b = b * reshape(norm_s([w]), shape_norm)
                    v = np.sum(b, axis=1) / b

                    # compute self-resemblance using matrix cosine similarity
                    sm = sm + np.exp( ( -1 + v ) / self.sigma**2 )

        # Final saliency map values
        sm = 1 / sm
        sm = sm.reshape(lark.shape[:-1])

        return sm


def main():

    seq = utils.load_gradient_mat('person01_boxing_d2_uncomp_64_64_40.mat')
    spaceTimeSaliencyMap = SpaceTimeSaliencyMap(seq=seq)
    sm = spaceTimeSaliencyMap.compute_saliency_map()

    print sm

if __name__ == '__main__':
    main()