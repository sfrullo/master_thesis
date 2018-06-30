# coding: utf-8

import logging
import numpy as np
import scipy.ndimage as ndi
import scipy.signal as sig

from time import time

def timeIt(func):
    def wrapper(*args, **kwargs):
        now = time()
        print "S - {}".format(func.__name__)
        result = func(*args, **kwargs)
        print "E - {} - time: {:.6f}s".format(func.__name__, time() - now)
        return result
    return wrapper

def to_column(x):
    return x.reshape(x.size, 1)

def edge_mirror_3(x, width=((3,), (3,), (3,))):
    # y = cat(2, x(:, width(2)+1:-1:2,:), x, x(: ,end-1:-1:end-width(2),:));
    # y = cat(1, y(width(1)+1:-1:2, :,:), y, y(end-1:-1:end-width(1), :,:));
    # z = cat(3, y(:,:,width(3)+1:-1:2), y, y(:,:,end-1:-1:end-width(3)));
    result = np.lib.pad(x, width, 'reflect')
    logging.info(result)
    return result

def gaussian(x, sx, y=None, sy=None):
    """Returns an array of numpy arrays (a matrix) containing values between
    1 and 0 in a 2D Gaussian distribution

    arguments
    x       -- width in pixels
    sx      -- width standard deviation

    keyword argments
    y       -- height in pixels (default = x)
    sy      -- height standard deviation (default = sx)
    """

    # square Gaussian if only x values are passed
    if y == None:
        y = x
    if sy == None:
        sy = sx
    # centers
    xo = x/2
    yo = y/2
    # matrix of zeros
    M = np.zeros([y,x],dtype=float)
    # gaussian matrix
    for i in range(x):
        for j in range(y):
            M[j,i] = np.exp(-1.0 * (((float(i)-xo)**2/(2*sx*sx)) + ((float(j)-yo)**2/(2*sy*sy)) ) )

    return M

def grid_density_gaussian_filter(x0, y0, x1, y1, w, h, data):

    r = 10

    kx = (w - 1) / float(x1 - x0)
    ky = (h - 1) / float(y1 - y0)

    borderw = w / 2
    borderh = h / 2
    imgw = (w + 2 * borderw)
    imgh = (h + 2 * borderh)
    img = np.zeros((imgh,imgw))

    for x, y, d in data:
        ix = int((x - x0) * kx) + borderw
        iy = int((y - y0) * ky) + borderh

        if 0 <= ix < imgw and 0 <= iy < imgh:
            img[iy][ix] += d

    heatmap = ndi.gaussian_filter(img, (r,r))  ## gaussian convolution

    return heatmap[borderh:h+borderh, borderw:w+borderw]

def moving_window_data_per_frame_generator(data, spf=1, ws=1):

    for i in range(0, len(data), int(spf)):
        past = data[i-ws:i,:,:]
        present = data[i,:,:]
        future = data[i+1:i+ws+1,:,:]

        frame_samples = np.vstack((past, present[np.newaxis,:], future))

        # print frame_samples
        yield np.concatenate(frame_samples, axis=0)

def resample(data, old_fps, new_fps):
    new_size = new_fps * data.size / old_fps
    return sig.resample(data, int(new_size))