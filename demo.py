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
from emosm.sm import gazesm

from emosm.tools import export

def main():

    dataset = mahnob.Mahnob()

    sessions = dataset.get_session_by_id(10)

    for sid, session in sessions.items():
        media = session.get_media()

    gaze_data = dataset.collect_gaze_data(sessions=sessions)

    print "coordinates shape: {}".format(gaze_data.get("coordinates").shape)
    print "fixations shape: {}".format(gaze_data.get("fixations").shape)

    offsets = [ i for i in range(0, media.metadata['nframes'], int(np.ceil(media.metadata['fps'] * 15)))]
    offsets = [ 0 ]

    gsm = gazesm.GazeSaliencyMap(gaze_data=gaze_data, media=media)
    gaze_saliency_map_generator = gsm.compute_saliency_map(limit_frame=300)

    # for frame_number, frame in enumerate(gaze_saliency_map_generator):
    #     print "Process frame #{}".format(frame_number)
    #     filename = "export/f{}.png".format(frame_number)
    #     # base_opts = { 'interpolation': 'nearest'}
    #     export.ToPNG(base=frame, filename=filename).export()

    export.ToVideo(frame_generator=gaze_saliency_map_generator, filename='export/s10.mp4').export()

    # sessions = dataset.get_sessions_by_mediafile("53.avi")
    # gaze_data = dataset.collect_gaze_data(sessions=sessions)

    # print "coordinates shape: {}".format(gaze_data.get("coordinates").shape)
    # print "fixations shape: {}".format(gaze_data.get("fixations").shape)

    # gsm = gazesm.GazeSaliencyMap()
    # gsm.set_gaze_data(gaze_data=gaze_data)
    # gsm.export_plot_on_media(media=media)

if __name__ == '__main__':
    main()