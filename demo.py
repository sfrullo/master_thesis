# coding: utf-8

# native
import os
import sys
sys.path.append("emosm")
sys.path.append("pyresemblance")
import glob
import time
import itertools

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

from pyresemblance import saliencymap as resemblancesm

from emosm.tools import export, utils

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

        gaze_data = mahnob.Mahnob.collect_gaze_data(sessions=sessions, mapped=True, preprocess=True)
        gaze_sm_gen = compute_gaze_sm(gaze_data=gaze_data, display_size=display_size, limit_frame=limit_frame)

        if destination in ["video"]:

            filename = config.VIDEO_EXPORT_DIR_BASE + '/gazesm_{}_{}.mp4'.format(media.get_name(), NOW)
            export.toVideo(sm_frame_gen=gaze_sm_gen, media_frames_gen=media_frames_gen, filename=filename, fps=media_fps)

        elif destination in ["return"]:

            return gaze_sm_gen

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

                return gaze_sm_gen


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


def export_composed_physiological_saliency_map(sessions, media, signals, psyco_construct, attribute, limit_frame, destination):

    ## COMPUTE AND EXPORT INTEGRATED PSYCOPHYSIOLOGICAL SALIENCY MAP FOR GIVEN SESSSION AND GIVEN SIGNALS

    media_frames_gen, media_fps, display_size = get_media_info(media=media, limit_frame=limit_frame)

    physio_sm_list = []

    gaze_data = mahnob.Mahnob.collect_gaze_data(sessions=sessions, mapped=True)
    physio_data = mahnob.Mahnob.collect_physiological_data(sessions=sessions, signals=signals)

    if limit_frame is None:
        max_sample = min([ d.stop - d.start for k,data in physio_data.items() for d in data ])
    else:
        max_sample = limit_frame

    for sigtype, data in physio_data.items():
        opts = {
            "sigtype" : sigtype,
            "attribute" : attribute,
            "psyco_construct" : psyco_construct,
            "fps" : media_fps,
            "max_sample" : max_sample,
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

        return composed_sm


def export_gaze_data_to_file(sessions, limit_frame):


    print "export_gaze_data_to_file"

    for sid, session in sessions.items():

        if glob.glob(config.DATA_EXPORT_DIR_BASE + "/gaze_data_{}*".format(sid)):

            print "data of session {} already present. skipped".format(sid)

        else:
            print "export data of session: {}".format(sid)

            session_info = session.get_session_info()

            gaze_data = session.get_gaze_data()

            coordinates_raw = gaze_data.get_gaze_coordinates(mapped=True)
            coordinates = gaze_data.get_gaze_coordinates(mapped=True, preprocess=True)

            fixations_raw = gaze_data.get_fixations_data()
            fixations = gaze_data.get_fixations_data(preprocess=True)

            data = {
                "session_info" : session_info,
                "coordinates_raw" : coordinates_raw,
                "coordinates" : coordinates,
                "fixations_raw" : fixations_raw,
                "fixations" : fixations,
            }

            filename = config.DATA_EXPORT_DIR_BASE + "/gaze_data_{}_{}.npz".format(sid, NOW)
            export.toBinaryFile(data=data, filename=filename, compressed=True)

            del session_info
            del gaze_data
            del data

def export_physio_data_to_file(sessions, limit_frame):

    print "export_physio_data_to_file"

    for sid, session in sessions.items():

        print "export data of session: {}".format(sid)

        session_info = session.get_session_info()

        physio_data = session.get_physiological_data(signals=["ECG","EDA","Resp","SKT"])

        if physio_data:
            signals = {}
            for signal, signal_class in physio_data.items():
                data = {}
                data["fps_raw"] = signal_class.metadata.info["sfreq"]
                data["raw"] = signal_class.get_data()

                # data["fps"] = 24
                data["processed"] = signal_class.get_data(preprocess=True, new_fps=signal_class.metadata.info["sfreq"])

                signals[signal.lower()] = data

        signals["pupil"] = session.get_gaze_data().get_pupil_size_data()

        data = dict(
            session_info=session_info,
            **signals
        )

        filename = config.DATA_EXPORT_DIR_BASE + "/physio_data_{}_{}.npz".format(sid, NOW)
        export.toBinaryFile(data=data, filename=filename, compressed=True)

        del physio_data
        del session_info
        del signals
        del data

def export_feature_data_to_file(sessions, limit_frame):

    print "export_feature_data_to_file"

    def pad_and_stack(feature_list):
        max_size = max(map(lambda x: np.size(x[1]), feature_list))
        stack = {}
        for feature_name, feature_data in feature_list:
            padded_data = np.pad(feature_data, (0,  max_size - feature_data.size), mode='constant', constant_values=np.nan)
            stack[feature_name] = padded_data
        return stack


    for sid, session in sessions.items():

        print "export data of session: {}".format(sid)

        session_info = session.get_session_info()

        all_signals = ["ECG","EDA","Resp","SKT"]
        all_psyco_construct = ["arousal", "valence"]
        all_attribute = ["mean", "std", "min", "max", "mean_diff", "mean_abs_diff"]

        physio_data = session.get_physiological_data(signals=all_signals)

        data = {
            "session_info" : session_info,
            "attributes" : all_attribute,
            "signals" : all_signals,
        }

        for psyco_construct in all_psyco_construct:
            feature_list = []
            for sigtype, sig_data in physio_data.items():
                for attribute in all_attribute:
                    opts = {
                        "sigtype" : sigtype,
                        "attribute" : attribute,
                        "psyco_construct" : psyco_construct,
                        "fps" : 24,
                    }

                    feature_name = sigtype + "_" + attribute
                    feature_data = fe.extract_physiological_feature(data=sig_data, opts=opts).flatten()

                    feature_list.append((feature_name, feature_data))

            data[psyco_construct] = pad_and_stack(feature_list)
            del feature_list

        filename = config.DATA_EXPORT_DIR_BASE + "/feature_data_{}_{}.npz".format(sid, NOW)
        export.toBinaryFile(data=data, filename=filename, compressed=True)

        del physio_data
        del session_info
        del data

def main():

    dataset = mahnob.Mahnob()

    sid_list = [10, 1042, 1044, 1046, 1048, 1050, 1052, 1054, 1056, 1058, 1060, 1062, 1064, 1066, 1068, 1172, 1174, 1176, 1178, 1180, 1182, 1184, 1186, 1188, 1190, 1192, 1194, 1196, 1198, 12, 1202, 1204, 1206, 1208, 1210,
132, 14, 142, 152, 1562, 1586, 1588, 1592, 1598, 16, 160, 166, 1692, 1694, 1696, 1698, 1700, 1702, 1704, 1706, 1708, 1710, 1712, 1714, 1716, 1718, 1720, 1722, 1724, 1726, 1728, 1730, 18, 1952, 1954, 1956, 1958,
1960, 1962, 1964, 1966, 1968, 1970, 1972, 1974, 1976, 1978, 1980, 1982, 2, 20, 2082, 2084, 2086, 2088, 2090, 2092, 2094, 2096, 2098, 2100, 2102, 2104, 2106, 2108, 2110, 2112, 2114, 2116, 2118, 2120, 22, 2212,
2214, 2216, 2218, 2220, 2222, 2224, 2226, 2228, 2230, 2232, 2234, 2236, 2238, 2240, 2242, 2244, 2246, 2248, 2250, 2342, 2352, 2354, 2358, 2376, 24, 2472, 2474, 2476, 2478, 2480, 2482, 2484, 2486, 2488, 2490,
2492, 2494, 2496, 2498, 2500, 2502, 2504, 2506, 2508, 2510, 26, 2602, 2604, 2606, 2608, 2610, 2612, 2614, 2616, 2618, 262, 2620, 2622, 2624, 2626, 2628, 2630, 2632, 2634, 2636, 2638, 264, 2640, 266, 268, 270,
272, 2732, 2734, 2736, 2738, 274, 2740, 2742, 2744, 2746, 2748, 2750, 2752, 2754, 2756, 2758, 276, 2760, 2762, 2764, 2766, 2768, 2770, 278, 28, 280, 282, 284, 286, 2862, 2864, 2866, 2868, 2870, 2872, 2874, 2876,
2878, 288, 2880, 2882, 2884, 2886, 2888, 2890, 2892, 2894, 2896, 2898, 290, 2900, 292, 294, 2992, 2994, 2996, 2998, 30, 3000, 3002, 3004, 3006, 3008, 3010, 3012, 3014, 3016, 3018, 3020, 3022, 3024, 3026, 3028,
3030, 3122, 3124, 3126, 3128, 3130, 3132, 3134, 3136, 3138, 3140, 3142, 3144, 3146, 3148, 3150, 3154, 3156, 3158, 3160, 32, 3382, 3384, 3386, 3388, 3390, 3392, 3394, 3396, 3398, 34, 3400, 3402, 3404, 3406,
3408, 3410, 3412, 3414, 3416, 3418, 3420, 3512, 3514, 3516, 3518, 3520, 3522, 3524, 3526, 3528, 3530, 3532, 3534, 3536, 3538, 3540, 3542, 3544, 3546, 3548, 3550, 36, 3646, 3664, 3668, 3670, 3680, 3772, 3774,
3776, 3778, 3780, 3782, 3784, 3786, 3788, 3790, 3792, 3794, 3796, 3798, 38, 3800, 3802, 3804, 3806, 3808, 3810, 398, 4, 40, 408, 420, 426, 430, 524, 530, 542, 546, 548, 6, 652, 654, 656, 658, 660, 662, 664, 666,
668, 670, 672, 674, 676, 678, 680, 682, 684, 686, 688, 690, 782, 784, 786, 788, 790, 792, 794, 796, 798, 8, 800, 802, 804, 806, 808, 810, 812, 814, 816, 818, 820, 920, 926, 932, 944, 948]

    # sessions = dataset.get_session_by_id(10)
    sessions = dataset.get_session_by_id(sorted(sid_list))
    # sessions = dataset.get_sessions_by_mediafile("53.avi")

    limit_frame = None

    # export_gaze_data_to_file(sessions=sessions, limit_frame=limit_frame)
    export_physio_data_to_file(sessions=sessions, limit_frame=limit_frame)
    #export_feature_data_to_file(sessions=sessions, limit_frame=limit_frame)



    # media_files = ["111.avi", "30.avi", "53.avi", "69.avi", "90.avi"]
    # for mediafile in media_files:

    #     sessions = dataset.get_sessions_by_mediafile(mediafile)

    #     #
    #     # EXPORT TO BINARY FILE
    #     #

    #     # export_gaze_data_to_file(sessions=sessions, limit_frame=limit_frame)
    #     export_physio_data_to_file(sessions=sessions, limit_frame=limit_frame)
    #     # export_feature_data_to_file(sessions=sessions, limit_frame=limit_frame)

    ##
    ## EXPORT GAZE SCANPATH FOR EACH SUBJECT
    ##

    # export_gaze_scanpath(sessions=sessions, limit_frame=limit_frame)

    ##
    ## COMPUTE GAZE SALIENCY MAP FOR EACH SUBJECT
    ##

    # export_gaze_sm(sessions=sessions, limit_frame=limit_frame, per_subject=True, destination="video")

    ##
    ## COMPUTE GAZE SALIENCY MAP USING ALL SUBJECTS
    ##

    # export_gaze_sm(sessions=sessions, limit_frame=limit_frame, per_subject=False, destination="video")

    # sm = export_gaze_sm(sessions=sessions, limit_frame=limit_frame, per_subject=False, destination="return")
    # filename = config.DATA_EXPORT_DIR_BASE + "/gaze_sm_{}.npz".format(NOW)
    # data = {
    #     "gaze_sm" : sm
    # }
    # export.toBinaryFile(data=data, filename=filename, compressed=True)


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

    # all_signals = ("ECG", "EDA", "Resp", "SKT")
    # all_psyco_construct = ["arousal", "valence"]
    # all_attribute = ["mean", "std"]

    # signal_combination = []
    # for s in map(set,itertools.product(all_signals, repeat=4)):
    #     if s not in signal_combination:
    #         signal_combination.append(s)

    # print sorted(signal_combination, key=len)

    # for signals, psyco_construct, attribute in itertools.product(signal_combination, all_psyco_construct, all_attribute):

    #     sm = export_composed_physiological_saliency_map(sessions=sessions, \
    #                                        media=media, \
    #                                        signals=signals, \
    #                                        psyco_construct=psyco_construct, \
    #                                        attribute=attribute, \
    #                                        limit_frame=limit_frame,
    #                                        destination="video")

        # break

        # data = { "physm" : list(sm) }
        # signals = "_".join(signals)
        # filename = config.DATA_EXPORT_DIR_BASE + "/physm_composed_{}_{}_{}_{}.npz".format(psyco_construct, attribute, signals, NOW)
        # export.toBinaryFile(data=data, filename=filename, compressed=True)


    ##
    ## COMPUTE SPATIO-TEMPORAL SALIENCY MAP
    ##

    # media = sessions.values()[0].get_media()
    # compute_resemblance_sm(media=media)

if __name__ == '__main__':

    main()
