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

    coordinates, fixations = dataset.collect_gaze_data(sessions=sessions)

    print coordinates
    print coordinates.shape


    sessions = dataset.get_sessions_by_mediafile("53.avi")
    coordinates, fixations = dataset.collect_gaze_data(sessions=sessions)

    print coordinates
    print coordinates.shape

    # gsm = gazesm.GazeSaliencyMap()
    # gsm.set_gaze_data(gaze_data=gaze_data)
    # gsm.export_plot_on_media(media=media)

if __name__ == '__main__':
    main()