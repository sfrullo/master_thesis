# coding: utf-8

# native
import os
import sys
sys.path.append("emosm")
import time

# external
import numpy as np
from matplotlib import pyplot as plt
import xmltodict

# custom
from emosm.dataset.mahnob import mahnob
from emosm.dataset.mahnob import config
from emosm.sm import gazesm, physiosm

from emosm.plot import gazeplot

import emosm.fe.feature_extractor as fe

from emosm.pyresemblance import saliencymap as resemblancesm

from emosm.tools import export

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

    filename = config.VIDEO_EXPORT_DIR_BASE + '/resemblance_sm_{}_{}.mp4'.format(media.get_name(), NOW)
    export.toVideo(sm_frame_gen=sm, media_frames_gen=media_frames, filename=filename, fps=media_fps)

def get_media_info(media, limit_frame=None):
    scale_media = config.SCALE_MEDIA
    display_size = media.get_size(scaled=scale_media)
    media_fps = media.metadata["fps"]
    media_frames_gen = media.get_frames(limit_frame=limit_frame, scale=scale_media, bw=True)
    return media_frames_gen, media_fps, display_size

def export_gaze_scanpath(sessions, limit_frame, destination):

    ## EXPORT GAZE SCANPATH FOR EACH SUBJECT

    for sid, session in sessions.items():

        media = session.get_media()
        media_frames_gen, media_fps, display_size = get_media_info(media=media, limit_frame=limit_frame)

        gaze_data = mahnob.Mahnob.collect_gaze_data(sessions={sid:session}, mapped=True)
        scanpath_generator = gazeplot.gaze_scanpath_plot_generator(gaze_data=gaze_data, limit_frame=limit_frame, fps=media_fps, display_size=display_size)

        if destination in ["video"]:

            filename = config.VIDEO_EXPORT_DIR_BASE + '/scanpath_{}_{}_{}.mp4'.format(sid, media.get_name(), NOW)
            export.toVideoSimple(data_frame_gen=scanpath_generator, media_frames_gen=media_frames_gen, filename=filename, fps=media_fps)

        elif destination in ["return"]:

            yield scanpath_generator


def compute_gaze_sm(gaze_data, display_size, limit_frame):
    gsm = gazesm.GazeSaliencyMap(gaze_data=gaze_data)
    gaze_sm_gen = gsm.compute_saliency_map(limit_frame=limit_frame, display_size=display_size)
    return gaze_sm_gen

def export_gaze_sm(sessions, limit_frame, per_subject, destination):
    ## COMPUTE GAZE SALIENCY MAP FOR EACH SUBJECT

    if per_subject is False:

        for sid, session in sessions.items():
            media = session.get_media()
            break

        media_frames_gen, media_fps, display_size = get_media_info(media=media, limit_frame=limit_frame)

        gaze_data = mahnob.Mahnob.collect_gaze_data(sessions=sessions, mapped=True)
        gaze_sm_gen = compute_gaze_sm(gaze_data=gaze_data, display_size=display_size, limit_frame=limit_frame)

        if destination in ["video"]:

            print "export_gaze_sm: export to video"

            filename = config.VIDEO_EXPORT_DIR_BASE + '/gazesm_{}_{}.mp4'.format(media.get_name(), NOW)
            export.toVideo(sm_frame_gen=gaze_sm_gen, media_frames_gen=media_frames_gen, filename=filename, fps=media_fps)

        elif destination in ["return"]:

            yield gaze_sm_gen

    else:

        for sid, session in sessions.items():

            media = session.get_media()
            media_frames_gen, media_fps, display_size = get_media_info(media=media, limit_frame=limit_frame)

            gaze_data = mahnob.Mahnob.collect_gaze_data(sessions={sid:session}, mapped=True)
            gaze_sm_gen = compute_gaze_sm(gaze_data=gaze_data, display_size=display_size, limit_frame=limit_frame)

            if destination in ["video"]:

                filename = config.VIDEO_EXPORT_DIR_BASE + '/gazesm_{}_{}_{}.mp4'.format(sid, media.get_name(), NOW)
                export.toVideo(sm_frame_gen=gaze_sm_gen, media_frames_gen=media_frames_gen, filename=filename, fps=media_fps)

            elif destination in ["return"]:

                yield gaze_sm_gen


def show_physiological_signals_in_sessions(sessions, signals):

    ## LOAD AND SHOW PHYSIOLOGICAL DATA FOR GIVEN SESSSION

    for sid, session in sessions.items():
        physio_data = session.get_physiological_data(signals=signals)
        for sigtype, data in physio_data.items():
            data.get_data(preprocess=True, show=True)


def export_separated_physiological_saliency_map(sessions, media, signals, psyco_construct_list, attribute_list, limit_frame, destination):

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

                if destination in ["video"]:

                    filename = config.VIDEO_EXPORT_DIR_BASE + '/physm_{}_{}_{}_{}.mp4'.format(psyco_construct, attribute, sigtype, NOW)
                    export.toVideo(sm_frame_gen=physio_sm_gen, media_frames_gen=media_frames_gen, filename=filename, fps=media_fps)

                elif destination in ["return"]:

                    yield physio_sm_gen


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

            if destination in ["video"]:

                signals = "_".join(signals)
                filename = config.VIDEO_EXPORT_DIR_BASE + '/physm_composed_{}_{}_{}_{}.mp4'.format(psyco_construct, attribute, signals, NOW)
                export.toVideo(sm_frame_gen=composed_sm, media_frames_gen=media_frames_gen, filename=filename, fps=media_fps)

            elif destination in ["return"]:

                yield physio_sm_gen


def export_session_data_to_file(sessions, limit_frame):

    print "export_session_data_to_file"

    for sid, session in sessions.items():

        session_info = session.get_session_info()
        gaze_data = mahnob.Mahnob.collect_gaze_data(sessions={sid:session}, mapped=True)
        sessions_gaze_sm = export_gaze_sm(sessions={sid:session}, limit_frame=limit_frame, per_subject=False, destination="return")

        data = {
            "session_info" : session_info,
            "coordinates" : gaze_data["coordinates"],
            "fixations" : gaze_data["fixations"],
            "gaze_sm" : list(sessions_gaze_sm)
        }

        filename = config.DATA_EXPORT_DIR_BASE + "/gaze_data_{}_{}.npz".format(sid, NOW)

        export.toBinaryFile(data=data, filename=filename, compressed=True)

        del session_info
        del gaze_data
        del sessions_gaze_sm
        del data


def main():

    dataset = mahnob.Mahnob()

    # sessions = dataset.get_session_by_id(10)
    # sessions = dataset.get_session_by_id([10,160])
    sessions = dataset.get_sessions_by_mediafile("53.avi")

    limit_frame = None

    ##
    ## EXPORT TO BINARY FILE
    ##

    export_session_data_to_file(sessions=sessions, limit_frame=limit_frame)

    ##
    ## EXPORT GAZE SCANPATH FOR EACH SUBJECT
    ##

    # export_gaze_scanpath(sessions=sessions, limit_frame=limit_frame)

    ##
    ## COMPUTE GAZE SALIENCY MAP FOR EACH SUBJECT
    ##

    # compute_gaze_sm(sessions=sessions, limit_frame=limit_frame, per_subject=True)

    ##
    ## COMPUTE GAZE SALIENCY MAP USING ALL SUBJECTS
    ##

    # compute_gaze_sm(sessions=sessions, limit_frame=limit_frame)

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
