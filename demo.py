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
    session = dataset.get_session_by_id(10)

    for sid, session in session.items():
        gaze_data, media = session.get_gaze_data(), session.get_media()
        gsm = gazesm.GazeSaliencyMap(gaze_data=gaze_data, media=media)

if __name__ == '__main__':
    main()