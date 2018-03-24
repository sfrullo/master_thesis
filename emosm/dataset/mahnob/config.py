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

BLINK_VALUES = np.float32(-1)