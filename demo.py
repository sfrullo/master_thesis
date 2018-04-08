# coding: utf-8

# native
import os, sys
sys.path.append("emosm")

# external
import xmltodict

# custom
from emosm.dataset.mahnob import mahnob
from emosm.plot import gazesm


def main():

    dataset = mahnob.Mahnob()

    sessions = dataset.get_session_by_id(10)

    for sid, session in sessions.items():
        media = session.get_media()

    gaze_data = dataset.collect_gaze_data(sessions=sessions)

    print "coordinates shape: {}".format(gaze_data.get("coordinates").shape)
    print "fixations shape: {}".format(gaze_data.get("fixations").shape)

    gsm = gazesm.GazeSaliencyMap(gaze_data=gaze_data, media=media)
    gsm.compute_saliency_map(show=True)


    # sessions = dataset.get_sessions_by_mediafile("53.avi")
    # gaze_data = dataset.collect_gaze_data(sessions=sessions)

    # print "coordinates shape: {}".format(gaze_data.get("coordinates").shape)
    # print "fixations shape: {}".format(gaze_data.get("fixations").shape)

    # gsm = gazesm.GazeSaliencyMap()
    # gsm.set_gaze_data(gaze_data=gaze_data)
    # gsm.export_plot_on_media(media=media)

if __name__ == '__main__':
    main()