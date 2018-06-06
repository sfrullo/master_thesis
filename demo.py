# coding: utf-8

# native
import os, sys
sys.path.append("emosm")

# external
import numpy as np
from matplotlib import pyplot as plt
import xmltodict

# custom
from emosm.dataset.mahnob import mahnob
from emosm.sm import gazesm, physiosm

from emosm.tools import export

import time

def main():

    dataset = mahnob.Mahnob()

    # sessions = dataset.get_session_by_id([10,160])
    sessions = dataset.get_sessions_by_mediafile("53.avi")

    for sid, session in sessions.items():
        media = session.get_media()

    ##
    ## EXPORT FIXATIONS BASED SALIENCY MAP
    ##

    gaze_data = dataset.collect_gaze_data(sessions=sessions)

    print "coordinates shape: {}".format(gaze_data.get("coordinates").shape)

    print "fixations shape: {}".format(gaze_data.get("fixations").shape)

    now = time.strftime("%y%m%d%H%M")

    # gsm = gazesm.GazeSaliencyMap(gaze_data=gaze_data, media=media)
    # gaze_saliency_map_generator = gsm.compute_saliency_map(limit_frame=3)

    # export.ToVideo(frame_generator=gaze_saliency_map_generator).export(filename='export/s10_24_{}.mp4'.format(now), fps=media.metadata["fps"])
    # export.ToVideo(frame_generator=gaze_saliency_map_generator).export(filename='export/s10_60_{}.mp4'.format(now), fps=media.metadata["fps"])

    ##
    ## LOAD PHYSIOLOGICAL DATA
    ##

    # for sid, session in sessions.items():
    #     physio_data = session.get_physiological_data(signals=["ECG"])
    #     for sigtype, data in physio_data.items():
    #         data.get_data(preprocess=True)

    physio_data = dataset.collect_physiological_data(sessions=sessions, signals=["ECG"])
    # print physio_data
    for sigtype, data in physio_data.items():
        for psyco_construct in ["valence", "arousal"]:
            for attribute in ["mean", "std"]:
                opts = {
                    "sigtype" : sigtype,
                    "attribute" : attribute,
                    "psyco_construct" : psyco_construct,
                    "fps" : media.metadata["fps"]
                }
                psm = physiosm.PhisioSaliencyMap(data=data, gaze=gaze_data, media=media, **opts)
                physio_saliency_map_generator = psm.compute_saliency_map(limit_frame=250)
                export.ToVideo(frame_generator=physio_saliency_map_generator).export(filename='export/{}_{}_{}_{}.mp4'.format(psyco_construct, attribute, sigtype, now), fps=opts["fps"])

if __name__ == '__main__':

    main()
    # dataset = mahnob.Mahnob()
    # sessions = dataset.get_session_by_id(10)

    # session = sessions[10]
    # data = session.get_gaze_data()