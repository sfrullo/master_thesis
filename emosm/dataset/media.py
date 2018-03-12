# coding: utf-8

import imageio

import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Media(object):
    """docstring for Media"""
    def __init__(self, filename, *arg, **kwarg):
        self.filename = filename

    def get_frames(self):
        with imageio.get_reader(self.filename) as reader:
            for frame in reader.iter_data():
                yield frame

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
    media.play()