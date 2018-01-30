# coding: utf-8

import numpy as np

# filter mask from MATLAB fspecial

# fspecial('disk', 1)
fspecial_disk_1 = np.array([
    [0.0251, 0.1453, 0.0251],
    [0.1453, 0.3183, 0.1453],
    [0.0251, 0.1453, 0.0251]
])