# coding: utf-8

import imageio

class Media(object):
    """docstring for Media"""
    def __init__(self, filename, *arg, **kwarg):
        self.filename = filename

    def get_frames(self):
        with imageio.get_reader(self.filename) as reader:
            for frame in reader.iter_data():
                yield frame
