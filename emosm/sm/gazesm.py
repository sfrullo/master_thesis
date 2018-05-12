# coding: utf-8

# native
import os
import os.path as path

# external
import numpy as np
import matplotlib.pyplot as plt

# custom
import emosm.tools.utils as utils
import emosm.tools.export as export
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

    def __compute_frame_saliency_map(self, fixations, display_size, mean_data=None):

        n_samples, data_dim = fixations.shape

        strt = self.gwh / 2
        heatmapsize = display_size[1] + 2*strt, display_size[0] + 2*strt
        heatmap = np.zeros(heatmapsize, dtype=float)

        # mean fixations in case of multiple sessions
        if mean_data is None:
            X, Y, D = fixations.T
        else:
            X, Y, D = fixations.mean(axis=0)

        for _x, _y in zip(X, Y):

            x = strt + int(_x) - int(strt)
            y = strt + int(_y) - int(strt)

            # correct Gaussian size if either coordinate falls outside of
            # display boundaries
            if not (0 < x < display_size[0]) or not (0 < y < display_size[1]):
                print "fix gaussian size for sample: x = {}, y = {}".format(_x, _y)

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
                    heatmap[y:y+vadj[1], x:x+hadj[1]] += self.gaus[vadj[0]:vadj[1], hadj[0]:hadj[1]]
                except:
                    # fixation was probably outside of display
                    pass

            else:
                # add Gaussian to the current heatmap
                heatmap[y:y+self.gwh, x:x+self.gwh] += self.gaus

        # resize heatmap
        heatmap = heatmap[strt:display_size[1]+strt, strt:display_size[0]+strt]

        # remove zeros
        lowbound = np.mean(heatmap[heatmap > 0])
        heatmap[heatmap < lowbound] = 0

        return heatmap

    def compute_saliency_map(self, limit_frame=None, show=False):
        print "start compute saliency map"

        fixations = self.gaze_data['fixations'] / config.FRAME_SCALE_FACTOR
        total_fixations_sample = self.gaze_data['fixations'].shape[0]

        display_size = self.media.get_scaled_size()
        n_frames = self.media.metadata['nframes']

        sample_per_frame = np.floor(total_fixations_sample / float(n_frames))

        if limit_frame is not None:
            stop = int(limit_frame * sample_per_frame)
            fixations = fixations[0:stop]

        framed_sample_generator = utils.moving_window_data_per_frame_generator(fixations, spf=sample_per_frame, ws=config.MIN_SAMPLE_WINDOW)
        media_frame = self.media.get_frames(limit_frame=limit_frame)

        print "Process frame"
        for frame_number, (framed_sample, frame) in enumerate(zip(framed_sample_generator, media_frame)):
            print "#{}".format(frame_number)
            frame_heatmap = self.__compute_frame_saliency_map(framed_sample, display_size)
            yield frame, frame_heatmap
        print "End"