# coding: utf-8

# native
import io

# external
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image

# custom
import emosm.tools.utils as utils

MAX_HISTORY_FIXATION = 5

def gaze_scanpath_plot_generator(gaze_data, limit_frame=None, fps=None, display_size=None):

    # dots per inch
    dpi = 100.0

    # determine the figure size in inches
    figsize = (display_size[0]/dpi, display_size[1]/dpi)

    # create a figure
    figure = plt.figure(figsize=figsize, dpi=dpi, frameon=False)

    ax = plt.Axes(figure, [0, 0, 1, 1])
    ax.set_axis_off()
    figure.add_axes(ax)

    fixations = gaze_data['fixations']

    if limit_frame is not None:
        fixations = fixations[:limit_frame]

    last_fixations = []

    def is_near(f1,f2):
        t = .5
        x, y, _ = abs(f1 - f2)
        if x <= t and y <= t:
            return True
        return False

    for frame_number, fixation in enumerate(fixations):
        print "# {}/{}".format(frame_number, fixations.shape[0])
        fixation = fixation[0]

        if len(last_fixations) > 0 and is_near(fixation, last_fixations[-1]):
            last_fixations[-1] += np.array([0, 0, 1])
        else:
            if len(last_fixations) > MAX_HISTORY_FIXATION:
                last_fixations.pop(0)
            fixation[2] = 1
            last_fixations.append(fixation)

        x, y, area = np.asarray(last_fixations).transpose()

        # plot display
        ax.clear()
        ax.axis([0, display_size[0], 0, display_size[1]])

        ax.plot(x, y, "b-", zorder=1)
        for x, y, s in last_fixations:
            t = ax.text(x=x, y=y, s=str(int(s)), ha="center", va="center", size=4, color="w", zorder=2)
            t.set_bbox(dict(boxstyle="circle,pad={}".format(s/10), fc='cyan', alpha=.2))

        ax.invert_yaxis()

        # create Image
        buf = io.BytesIO()
        plt.savefig(buf, format="png", frameon=False, transparent=True)
        buf.seek(0)
        im = Image.open(buf).convert("RGBA")
        buf.close()

        yield im
