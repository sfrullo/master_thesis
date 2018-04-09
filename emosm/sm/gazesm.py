# coding: utf-8

# native
import os
import os.path as path

# external
import numpy as np
import matplotlib.pyplot as plt

# custom
import emosm.tools.utils as utils
import emosm.dataset.mahnob.config as config


class GazeSaliencyMap(object):
    """docstring for GazeSaliencyMap"""
    def __init__(self, gaze_data=None, media=None, *arg, **kwarg):
        super(GazeSaliencyMap, self).__init__()
        self.gaze_data = gaze_data
        self.media = media

        self.gwh = config.GAUSSIAN_WIDTH
        self.gsdwh = config.GAUSSIAN_STD_DEV
        self.gaus = utils.gaussian(self.gwh, self.gsdwh)

    def set_gaze_data(self, gaze_data):
        self.gaze_data = gaze_data

    def set_media(self, media):
        self.media = media

    def __compute_frame_saliency_map(self, fixations, display_size):

        n_samples, n_subject, data_dim = fixations.shape

        strt = self.gwh / 2
        heatmapsize = display_size[1] + 2*strt, display_size[0] + 2*strt
        heatmap = np.zeros(heatmapsize, dtype=float)

        for i in xrange(0, n_samples):
            data = fixations[i]

            # mean data in case of multiple sessions
            _x, _y, dur = data.mean(axis=0)

            x = strt + int(_x) - int(strt)
            y = strt + int(_y) - int(strt)

            # correct Gaussian size if either coordinate falls outside of
            # display boundaries
            if not (0 < x < display_size[0]) or not (0 < y < display_size[1]):
                print "fix gaussian size for sample #{}: x = {}, y = {}".format(i, _x, _y)

                hadj = [0, self.gwh]
                vadj = [0, self.gwh]

                if 0 > x:
                    hadj[0], x = abs(x), 0
                elif display_size[0] < x:
                    hadj[1] = self.gwh - int(x - display_size[0])

                if 0 > y:
                    vadj[0], y = abs(y), 0
                elif display_size[1] < y:
                    vadj[1] = self.gwh - int(y - display_size[1])

                # add adjusted Gaussian to the current heatmap
                try:
                    heatmap[y:y+vadj[1], x:x+hadj[1]] += self.gaus[vadj[0]:vadj[1], hadj[0]:hadj[1]] * dur
                except:
                    # fixation was probably outside of display
                    pass

            else:
                # add Gaussian to the current heatmap
                heatmap[y:y+self.gwh, x:x+self.gwh] += self.gaus * dur

        # resize heatmap
        heatmap = heatmap[strt:display_size[1]+strt, strt:display_size[0]+strt]

        # remove zeros
        lowbound = np.mean(heatmap[heatmap > 0])
        heatmap[heatmap < lowbound] = np.nan

        return heatmap

    def compute_saliency_map(self, show=False):
        print "start compute saliency map"

        fixations = self.gaze_data['fixations']
        n_samples, n_subject, data_dim = fixations.shape

        display_size = self.media.metadata['size']
        n_frames = self.media.metadata['nframes']

        sample_per_frame = n_samples / float(n_frames)

        heatmap = self.__compute_frame_saliency_map(fixations, display_size)

        if show:
            dpi = 100
            figsize = display_size[0]/dpi, display_size[1]/dpi
            fig = plt.figure(figsize=figsize, dpi=dpi)
            ax = plt.Axes(fig, [0,0,1,1])
            ax.set_axis_off()
            fig.add_axes(ax)
            ax.imshow(heatmap, cmap='jet')

        return heatmap