# coding: utf-8

# native
import os
import sys
sys.path.append("emosm")

# external
import numpy as np
from matplotlib import pyplot as plt
import xmltodict

# custom
from emosm.dataset.mahnob import mahnob
from emosm.dataset.mahnob import config
from emosm.sm import gazesm, physiosm

from emosm.pyresemblance import saliencymap as resemblancesm

from emosm.tools import export

import time

def compute_resemblance_sm(media):

    ## COMPUTE AND EXPORT PYRESAMBLANCE SALIENCY MAP FOR A GIVE MEDIA

    limit_frame = 40

    scale_media = False
    display_size = media.get_size(scaled=scale_media)
    media_fps = media.metadata["fps"]
    media_frames_gen = media.get_frames(limit_frame=limit_frame, scale=scale_media, bw=True)

    media_frames = np.array(list(media_frames_gen))

    spaceTimeSaliencyMap = resemblancesm.SpaceTimeSaliencyMap(seq=media_frames)
    sm = spaceTimeSaliencyMap.compute_saliency_map()

    now = time.strftime("%y%m%d%H%M")

    filename = 'export/resemblance_sm_{}_{}.mp4'.format(media.get_name(), now)
    export.toVideo(sm_frame_gen=sm, media_frames_gen=media_frames, filename=filename, fps=media_fps)


def compute_gaze_sm_per_subject(sessions, limit_frame):

    ## COMPUTE GAZE SALIENCY MAP FOR EACH SUBJECT

    for sid, session in sessions.items():
        media = session.get_media()

        scale_media = config.SCALE_MEDIA
        display_size = media.get_size(scaled=scale_media)
        media_fps = media.metadata["fps"]
        media_frames_gen = media.get_frames(limit_frame=limit_frame, scale=scale_media)

        gaze_data = dataset.collect_gaze_data(sessions={sid:session}, mapped=True)

        gsm = gazesm.GazeSaliencyMap(gaze_data=gaze_data)
        gaze_sm_gen = gsm.compute_saliency_map(limit_frame=limit_frame, display_size=display_size)

        filename = 'export/video/gazesm_sub_{}_{}_{}.mp4'.format(sid, media.get_name(), now)
        export.toVideo(sm_frame_gen=gaze_sm_gen, media_frames_gen=media_frames_gen, filename=filename, fps=media_fps)


def compute_gaze_sm_using_all_subjects(gaze_data, media, limit_frame)

    ## COMPUTE GAZE SALIENCY MAP USING ALL SUBJECTS

    print "coordinates shape: {}".format(gaze_data.get("coordinates").shape)
    print "fixations shape: {}".format(gaze_data.get("fixations").shape)

    gsm = gazesm.GazeSaliencyMap(gaze_data=gaze_data)
    gaze_sm_gen = gsm.compute_saliency_map(limit_frame=limit_frame, display_size=display_size)

    filename = 'export/gazesm_{}_{}.mp4'.format(media.get_name(), now)
    export.toVideo(sm_frame_gen=gaze_sm_gen, media_frames_gen=media_frames_gen, filename=filename, fps=media_fps)


def show_physiological_signals_in_sessions(sessions, signals):

    ## LOAD AND SHOW PHYSIOLOGICAL DATA FOR GIVEN SESSSION

    for sid, session in sessions.items():
        physio_data = session.get_physiological_data(signals=signals)
        for sigtype, data in physio_data.items():
            data.get_data(preprocess=True, show=True)


def export_separated_physiological_saliency_map(sessions, media, signals, psyco_construct, attribute, limit_frame)

    ## COMPUTE AND EXPORT SEPARATED PSYCOPHYSIOLOGICAL SALIENCY MAP FOR GIVEN SESSSION AND GIVEN SIGNALS

    physio_data = dataset.collect_physiological_data(sessions=sessions, signals=signals)
    for sigtype, data in physio_data.items():
        for psyco_construct in psyco_construct:
            for attr in attribute:
                opts = {
                    "sigtype" : sigtype,
                    "attribute" : attr,
                    "psyco_construct" : psy,
                    "fps" : media_fps
                }

                psm = physiosm.PhysioSaliencyMap(data=data, gaze=gaze_data, media=media, **opts)
                physio_sm_gen = psm.compute_saliency_map(limit_frame=limit_frame, display_size=display_size)

                filename = 'export/{}_{}_{}_{}.mp4'.format(psy, attr, sigtype, now)
                export.toVideo(sm_frame_gen=physio_sm_gen, media_frames_gen=media_frames_gen, filename=filename, fps=opts["fps"])


def export_composed_physiological_saliency_map(sessions, media, signals, psyco_construct, attribute, limit_frame)

    ## COMPUTE AND EXPORT INTEGRATED PSYCOPHYSIOLOGICAL SALIENCY MAP FOR GIVEN SESSSION AND GIVEN SIGNALS

    physio_data = dataset.collect_physiological_data(sessions=sessions, signals=signals)
    for psyco_construct in ["arousal"]:
        for attribute in ["std"]:
            physio_sm_list = []
            for sigtype, data in physio_data.items():
                opts = {
                    "sigtype" : sigtype,
                    "attribute" : attribute,
                    "psyco_construct" : psyco_construct,
                    "fps" : media.metadata["fps"]
                }
                psm = physiosm.PhysioSaliencyMap(data=data, gaze=gaze_data, media=media, **opts)
                physio_sm_gen = psm.compute_saliency_map(limit_frame=limit_frame, display_size=display_size)
                physio_sm_list.append(physio_sm_gen)

            # create generator to integrate framed physiological data
            composed_sm = physiosm.physioSaliencyMapComposer(physio_sm_list)

            signals = "_".join(signals)
            filename = 'export/composed_{}_{}_{}_{}.mp4'.format(psyco_construct, attribute, signals, now)
            export.toVideo(sm_frame_gen=composed_sm, media_frames_gen=media_frames_gen, filename=filename, fps=opts["fps"])


def main():

    dataset = mahnob.Mahnob()

    sessions = dataset.get_session_by_id(10)
    # sessions = dataset.get_session_by_id([10,160])
    # sessions = dataset.get_sessions_by_mediafile("53.avi")

    for sid, session in sessions.items()[0]:
        media = session.get_media()

    ##
    ## EXPORT FIXATIONS BASED SALIENCY MAP
    ##

    now = time.strftime("%y%m%d%H%M")

    limit_frame = 500

    scale_media = config.SCALE_MEDIA
    display_size = media.get_size(scaled=scale_media)
    media_fps = media.metadata["fps"]
    media_frames_gen = media.get_frames(limit_frame=limit_frame, scale=scale_media)

    ##
    ## COMPUTE GAZE SALIENCY MAP FOR EACH SUBJECT
    ##

    # compute_gaze_sm_per_subject(sessions=sessions)

    ##
    ## COMPUTE GAZE SALIENCY MAP USING ALL SUBJECTS
    ##

    # gaze_data = dataset.collect_gaze_data(sessions=sessions, mapped=True)
    # compute_gaze_sm_using_all_subjects(gaze_data=gaze_data, media=media)

    ##
    ## LOAD AND SHOW PHYSIOLOGICAL DATA FOR GIVEN SESSSION
    ##

    # signals=["SKT"]
    # show_physiological_signals_in_sessions(sessions=sessions, signals=signals)

    ##
    ## COMPUTE AND EXPORT SEPARATED PSYCOPHYSIOLOGICAL SALIENCY MAP FOR GIVEN SESSSION AND GIVEN SIGNALS
    ##

    signals=["EDA"]
    psyco_construct=["arousal"]
    attribute=["mean"]
    export_separated_physiological_saliency_map(sessions=sessions, \
                                                media=media, \
                                                signals=signals, \
                                                psyco_construct=psyco_construct, \
                                                attribute=attribute, \
                                                limit_frame=limit_frame)

    ##
    ## COMPUTE AND EXPORT INTEGRATED PSYCOPHYSIOLOGICAL SALIENCY MAP FOR GIVEN SESSSION AND GIVEN SIGNALS
    ##

    signals = ["EDA","SKT"]
    psyco_construct = ["arousal"]
    attribute = ["std"]
    export_composed_physiological_saliency_map(sessions=sessions, \
                                               media=media, \
                                               signals=signals, \
                                               psyco_construct=psyco_construct, \
                                               attribute=attribute, \
                                               limit_frame=limit_frame)

    ##
    ## COMPUTE SPATIO-TEMPORAL SALIENCY MAP
    ##

    # compute_resemblance_sm(media=media)

if __name__ == '__main__':

    main()
