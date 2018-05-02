# coding: utf-8

import os
import numpy as np

#
# MAHNOB DIRECTORIES
#

DIR_BASE = '/media/sf_vbfolder/TesiCastellani/Dataset/Mahnob'
DIR_MAHNOB = {
    'MediaFiles' : os.path.join(DIR_BASE, 'data/MediaFiles'),
    'Sessions' : os.path.join(DIR_BASE, 'data/Sessions'),
    'Subjects' : os.path.join(DIR_BASE, 'data/Subjects'),
}

#
# Gaze Data Constants
#

HEADER_LENGTH = 24
SAMPLE_RATE = 60

BLINK_VALUES = np.float32(-1.0)

#
# Media Processing Consts
#

FRAME_SCALE_FACTOR = 2

#
# GazeSaliencyMaps Constants
#

MIN_SAMPLE_WINDOW = 2

GAUSSIAN_WIDTH = 200 / FRAME_SCALE_FACTOR
GAUSSIAN_STD_DEV = GAUSSIAN_WIDTH / 6