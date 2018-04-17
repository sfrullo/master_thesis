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
    frame_saliency_map_generator = gsm.compute_saliency_map()
    sm = next(frame_saliency_map_generator)

    for offset in offsets:
        limit_frame = 5 + offset
        counter = 0
        for frame in media.get_frames(n_frame=limit_frame):

            if counter > offset:
                print "Process frame #{}".format(counter)
                filename = "export/f{}.png".format(counter)

                sm = next(frame_saliency_map_generator)

                base_opts = { 'cmap': plt.cm.gray, 'interpolation': 'nearest'}
                sm_opts = { 'cmap': plt.cm.jet, 'alpha': .5}

                export.ToPNG(base=frame, base_opts=base_opts, overlays=[sm], overlays_opts=[sm_opts], filename=filename).export()

            counter += 1


    # sessions = dataset.get_sessions_by_mediafile("53.avi")
    # gaze_data = dataset.collect_gaze_data(sessions=sessions)

    # print "coordinates shape: {}".format(gaze_data.get("coordinates").shape)
    # print "fixations shape: {}".format(gaze_data.get("fixations").shape)

    # gsm = gazesm.GazeSaliencyMap()
    # gsm.set_gaze_data(gaze_data=gaze_data)
    # gsm.export_plot_on_media(media=media)

if __name__ == '__main__':
    main()