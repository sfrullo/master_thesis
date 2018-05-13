# coding: utf-8

# native
import imageio

# external
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from PIL import Image

# custom
import emosm.dataset.mahnob.config as config


class Media(object):
    """docstring for Media"""
    def __init__(self, filename, *arg, **kwarg):
        self.filename = filename

        # self.metadata = {}
        #     'ffmpeg_version': u'2.8.11-0ubuntu0.16.04.1 built with gcc 5.4.0 (Ubuntu 5.4.0-6ubuntu1~16.04.4) 20160609',
        #     'plugin': 'ffmpeg',
        #     'source_size': (1280, 800),
        #     'nframes': 2733,
        #     'fps': 23.98,
        #     'duration': 113.95,
        #     'size': (1280, 800),
        # }
        self.metadata = imageio.get_reader(self.filename).get_meta_data()
        self.scaling_factor = config.FRAME_SCALE_FACTOR

    def get_size(self, scaled=False):
        if not scaled:
            return self.metadata['size']
        return self.metadata['size'][0]/config.FRAME_SCALE_FACTOR, self.metadata['size'][1]/config.FRAME_SCALE_FACTOR

    def get_frames(self, limit_frame=None, scale=False):
        """ Get media frame.

            params:
                limit_frame    : how many frames to generate. limit_frame = 0 generate all frames in media

         """
        current_frame = 0
        with imageio.get_reader(self.filename) as reader:
            for frame in reader.iter_data():
                if limit_frame is not None and current_frame > limit_frame:
                    raise StopIteration
                else:
                    image = Image.fromarray(frame)
                    if scale:
                        image = image.resize(self.get_scaled_size(), resample=Image.NEAREST)
                    yield np.array(image)
                    current_frame += 1

    def play(self):
        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1)

        def animate(frame):
            ax1.clear()
            ax1.imshow(frame)

        ani = animation.FuncAnimation(fig, func=animate, frames=self.get_frames, interval=1000/60.0)
        plt.show()

if __name__ == '__main__':

    media = Media(filename="/media/sf_vbfolder/TesiCastellani/Dataset/Mahnob/data/MediaFiles/111.avi")
    print media.metadata
    media.play()