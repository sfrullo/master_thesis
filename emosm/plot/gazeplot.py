# coding: utf-8

# native

# external
import numpy as np
import matplotlib.pyplot as plt

# custom
import emosm.tools.utils as utils

MAX_HISTORY_FIXATION = 5

def gaze_scanpath_plot_generator(gaze_data, limit_frame=None, fps=None, display_size=None):

    fixations = gaze_data['fixations']

    if limit_frame is not None:
        fixations = fixations[:limit_frame]

    last_fixations = []

    for frame_number, fixation in enumerate(fixations):
        print "# {}/{}".format(frame_number, fixations.shape[0])
        fixation = fixation[0]

        if len(last_fixations) and np.array_equal(fixation, last_fixations[-1]):
            last_fixations[-1] += np.array([0, 0, 1])
        else:
            if len(last_fixations) > MAX_HISTORY_FIXATION:
                last_fixations.pop(0)
            last_fixations.append(fixation)

        x, y, area = np.asarray(last_fixations).transpose()

        # dots per inch
        dpi = 100.0
        # determine the figure size in inches
        figsize = (display_size[0]/dpi, display_size[1]/dpi)

        # create a figure
        figure = plt.figure(figsize=figsize, dpi=dpi, frameon=False)

        ax = plt.Axes(figure, [0,0,1,1])

        ax.set_axis_off()
        figure.add_axes(ax)
        # plot display
        ax.axis([0,display_size[0],0,display_size[1]])
        # ax.plot(y,x)
        ax.scatter(x=x, y=y, s=area, alpha=.5, zorder=1)
        ax.invert_yaxis()

        # plt.show()

        data = utils.fig2data(figure)

        # print data.shape

        data = np.swapaxes(data,0,1)

        yield data