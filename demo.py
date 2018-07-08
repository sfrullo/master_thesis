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

import emosm.fe.feature_extractor as fe

from emosm.pyresemblance import saliencymap as resemblancesm

from emosm.tools import export

import time

NOW = time.strftime("%y%m%d%H%M")

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

    filename = 'export/resemblance_sm_{}_{}.mp4'.format(media.get_name(), NOW)
    export.toVideo(sm_frame_gen=sm, media_frames_gen=media_frames, filename=filename, fps=media_fps)

def get_media_info(media, limit_frame=None):
    scale_media = config.SCALE_MEDIA
    display_size = media.get_size(scaled=scale_media)
    media_fps = media.metadata["fps"]
    media_frames_gen = media.get_frames(limit_frame=limit_frame, scale=scale_media)
    return media_frames_gen, media_fps, display_size

def export_gaze_sm(gaze_data, media, limit_frame, filename):

    media_frames_gen, media_fps, display_size = get_media_info(media=media, limit_frame=limit_frame)

    gsm = gazesm.GazeSaliencyMap(gaze_data=gaze_data)
    gaze_sm_gen = gsm.compute_saliency_map(limit_frame=limit_frame, display_size=display_size)
    export.toVideo(sm_frame_gen=gaze_sm_gen, media_frames_gen=media_frames_gen, filename=filename, fps=media_fps)


def compute_gaze_sm(sessions, limit_frame, per_subject=False):

    ## COMPUTE GAZE SALIENCY MAP FOR EACH SUBJECT

    if per_subject is False:

        for sid, session in sessions.items():
            media = session.get_media()
            break

        gaze_data = mahnob.Mahnob.collect_gaze_data(sessions=sessions, mapped=True)
        filename = 'export/gazesm_{}_{}.mp4'.format(media.get_name(), NOW)
        export_gaze_sm(gaze_data=gaze_data, media=media, limit_frame=limit_frame, filename=filename)

    else:

        for sid, session in sessions.items():
            media = session.get_media()
            gaze_data = mahnob.Mahnob.collect_gaze_data(sessions={sid:session}, mapped=True)
            filename = 'export/gazesm_{}_{}_{}.mp4'.format(sid, media.get_name(), NOW)
            export_gaze_sm(gaze_data=gaze_data, media=media, limit_frame=limit_frame, filename=filename)


def show_physiological_signals_in_sessions(sessions, signals):

    ## LOAD AND SHOW PHYSIOLOGICAL DATA FOR GIVEN SESSSION

    for sid, session in sessions.items():
        physio_data = session.get_physiological_data(signals=signals)
        for sigtype, data in physio_data.items():
            data.get_data(preprocess=True, show=True)


def export_separated_physiological_saliency_map(sessions, media, signals, psyco_construct_list, attribute_list, limit_frame):

    ## COMPUTE AND EXPORT SEPARATED PSYCOPHYSIOLOGICAL SALIENCY MAP FOR GIVEN SESSSION AND GIVEN SIGNALS

    media_frames_gen, media_fps, display_size = get_media_info(media=media, limit_frame=limit_frame)

    gaze_data = mahnob.Mahnob.collect_gaze_data(sessions=sessions, mapped=True)
    physio_data = mahnob.Mahnob.collect_physiological_data(sessions=sessions, signals=signals)
    for sigtype, data in physio_data.items():
        for psyco_construct in psyco_construct_list:
            for attribute in attribute_list:
                opts = {
                    "sigtype" : sigtype,
                    "attribute" : attribute,
                    "psyco_construct" : psyco_construct,
                    "fps" : media_fps
                }

                features = fe.extract_physiological_feature(data=data, opts=opts)
                psm = physiosm.PhysioSaliencyMap(physio=features, gaze=gaze_data, media=media)
                physio_sm_gen = psm.compute_saliency_map(limit_frame=limit_frame, display_size=display_size)

                filename = 'export/physm_{}_{}_{}_{}.mp4'.format(psyco_construct, attribute, sigtype, NOW)
                export.toVideo(sm_frame_gen=physio_sm_gen, media_frames_gen=media_frames_gen, filename=filename, fps=media_fps)


def export_composed_physiological_saliency_map(sessions, media, signals, psyco_construct_list, attribute_list, limit_frame):

    ## COMPUTE AND EXPORT INTEGRATED PSYCOPHYSIOLOGICAL SALIENCY MAP FOR GIVEN SESSSION AND GIVEN SIGNALS

    media_frames_gen, media_fps, display_size = get_media_info(media=media, limit_frame=limit_frame)

    gaze_data = mahnob.Mahnob.collect_gaze_data(sessions=sessions, mapped=True)
    physio_data = mahnob.Mahnob.collect_physiological_data(sessions=sessions, signals=signals)
    for psyco_construct in psyco_construct_list:
        for attribute in attribute_list:
            physio_sm_list = []
            for sigtype, data in physio_data.items():
                opts = {
                    "sigtype" : sigtype,
                    "attribute" : attribute,
                    "psyco_construct" : psyco_construct,
                    "fps" : media_fps
                }

                features = fe.extract_physiological_feature(data=data, opts=opts)
                psm = physiosm.PhysioSaliencyMap(physio=features, gaze=gaze_data, media=media)
                physio_sm_gen = psm.compute_saliency_map(limit_frame=limit_frame, display_size=display_size)
                physio_sm_list.append(physio_sm_gen)

            # create generator to integrate framed physiological data
            composed_sm = physiosm.physioSaliencyMapComposer(physio_sm_list)

            signals = "_".join(signals)
            filename = 'export/physm_composed_{}_{}_{}_{}.mp4'.format(psyco_construct, attribute, signals, NOW)
            export.toVideo(sm_frame_gen=composed_sm, media_frames_gen=media_frames_gen, filename=filename, fps=media_fps)


def main():

    dataset = mahnob.Mahnob()

    sessions = dataset.get_session_by_id(10)
    # sessions = dataset.get_session_by_id([10,160])
    # sessions = dataset.get_sessions_by_mediafile("53.avi")

    limit_frame = 200

    ##
    ## COMPUTE GAZE SALIENCY MAP FOR EACH SUBJECT
    ##

    # compute_gaze_sm(sessions=sessions, limit_frame=limit_frame, per_subject=True)

    ##
    ## COMPUTE GAZE SALIENCY MAP USING ALL SUBJECTS
    ##

    compute_gaze_sm(sessions=sessions, limit_frame=limit_frame)

    ##
    ## LOAD AND SHOW PHYSIOLOGICAL DATA FOR GIVEN SESSSION
    ##

    # signals=["SKT"]
    # show_physiological_signals_in_sessions(sessions=sessions, signals=signals)

    ##
    ## EXPORT PHYSIOLOGICAL SALIENCY MAP
    ##

    # for sid, session in sessions.items():
    #     media = session.get_media()
    #     break

    # scale_media = config.SCALE_MEDIA
    # display_size = media.get_size(scaled=scale_media)
    # media_fps = media.metadata["fps"]
    # media_frames_gen = media.get_frames(limit_frame=limit_frame, scale=scale_media)

    ##
    ## COMPUTE AND EXPORT SEPARATED PSYCOPHYSIOLOGICAL SALIENCY MAP FOR GIVEN SESSSION AND GIVEN SIGNALS
    ##

    # signals=["EDA"]
    # psyco_construct=["valence"]
    # attribute=["mean"]
    # export_separated_physiological_saliency_map(sessions=sessions, \
    #                                             media=media, \
    #                                             signals=signals, \
    #                                             psyco_construct_list=psyco_construct, \
    #                                             attribute_list=attribute, \
    #                                             limit_frame=limit_frame)

    ##
    ## COMPUTE AND EXPORT INTEGRATED PSYCOPHYSIOLOGICAL SALIENCY MAP FOR GIVEN SESSSION AND GIVEN SIGNALS
    ##

    # signals = ["EDA","SKT"]
    # psyco_construct = ["arousal"]
    # attribute = ["std"]
    # export_composed_physiological_saliency_map(sessions=sessions, \
    #                                            media=media, \
    #                                            signals=signals, \
    #                                            psyco_construct_list=psyco_construct, \
    #                                            attribute_list=attribute, \
    #                                            limit_frame=limit_frame)

    ##
    ## COMPUTE SPATIO-TEMPORAL SALIENCY MAP
    ##

    # compute_resemblance_sm(media=media)

if __name__ == '__main__':

    main()
