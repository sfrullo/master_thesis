# coding: utf-8

import numpy as np

from matplotlib import pyplot as plt
from matplotlib import image as mpimg
from matplotlib import animation


class ToVideo(object):

    def __init__(self, base=None, base_opts={}, overlays=[], overlays_opts=[], filename='export.mp4', *args, **kwargs):

        if base is None:
            raise ValueError('base must be valid sequence of frames')

        self.base = base
        self.base_opts = base_opts

        self.overlays = overlays
        if not isinstance(overlays, list):
            self.overlays = [overlays]

        self.overlays_opts = overlays_opts
        if not isinstance(overlays_opts, list):
            self.overlays_opts = [overlays_opts]

        for index, overlay in enumerate(self.overlays):
            if overlay.shape != self.base.shape:
                raise ValueError('base and overlay #{} shapes differ')

        # First set up the figure, the axis, and the plot element we want to animate
        self.main_figure = plt.figure()

        # frames is a list containg all the frames to draw
        self.frames = self.get_frames()

        self.filename = filename

    # initialization function: compute each frame
    def get_frames(self):
        frames_list = []
        for i in range(self.base.shape[-1]):
            frame = []
            base_figure = plt.imshow(self.base[:,:,i], **self.base_opts)
            frame.append(base_figure)
            for overlay, opts in zip(self.overlays, self.overlays_opts):
                overlays_figure = plt.imshow(overlay[:,:,i], **opts)
                frame.append(overlays_figure)
            frames_list.append(frame)
        return frames_list

    def export(self):
        fig = self.main_figure
        frames = self.frames
        ani = animation.ArtistAnimation(fig, frames, interval=50, blit=True, repeat_delay=1000)
        ani.save(self.filename)

def main():

    import matio
    seq = matio.load_mat_file('person01_boxing_d2_uncomp_64_64_40.mat')
    sm = matio.load_mat_file('SM.mat')

    # w = np.s_[:,:,0]
    # fig1 = plt.imshow(seq[w], interpolation='nearest', cmap=plt.cm.gray)
    # fig2 = plt.imshow(sm[w], alpha=.8, cmap=plt.cm.jet)

    # plt.show()
    base_opts = { 'cmap': plt.cm.gray, 'interpolation': 'nearest', 'animated': True }
    sm_opts = { 'cmap': plt.cm.jet, 'alpha': .5, 'animated': True }
    toVideo = ToVideo(base=seq, base_opts=base_opts, overlays=[sm], overlays_opts=[sm_opts])
    toVideo.export()

if __name__ == '__main__':
    main()