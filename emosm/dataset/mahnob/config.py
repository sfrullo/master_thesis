# coding: utf-8

import os
import numpy as np

#
# MAHNOB DIRECTORIES
#

DIR_BASE = '/media/sf_vbfolder/TesiCastellani/Dataset/Mahnob'
DIR_MAHNOB = {
    # 'MediaFiles' : os.path.join(DIR_BASE, 'data/MediaFiles'),
    'MediaFiles' : os.path.join(DIR_BASE, 'data/media_24'),
    'Sessions' : os.path.join(DIR_BASE, 'data/Sessions'),
    'Subjects' : os.path.join(DIR_BASE, 'data/Subjects'),
}

EXPORT_DIR_BASE = "/media/sf_vbfolder/TesiCastellani/export"
VIDEO_EXPORT_DIR_BASE = os.path.join(EXPORT_DIR_BASE, "video")
DATA_EXPORT_DIR_BASE = os.path.join(EXPORT_DIR_BASE, "data")

try:
	os.makedirs(VIDEO_EXPORT_DIR_BASE)
except OSError:
	pass

try:
	os.makedirs(DATA_EXPORT_DIR_BASE)
except OSError:
	pass

#
# Gaze Data Constants
#

HEADER_LENGTH = 24
EYE_TRACKING_SAMPLE_RATE = 60

BLINK_VALUES = np.float32(-1.0)

#
# Media Processing Consts
#

MEDIA_FPS = 24
SCALE_MEDIA = False
FRAME_SCALE_FACTOR = 4  # this factor will scale also the gaze's coordinates, thus it must be coherent with both the video and gaze display size

#
# GazeSaliencyMaps Constants
#

MIN_SAMPLE_WINDOW = 1

GAUSSIAN_WIDTH = 200 / FRAME_SCALE_FACTOR
GAUSSIAN_STD_DEV = GAUSSIAN_WIDTH / 12