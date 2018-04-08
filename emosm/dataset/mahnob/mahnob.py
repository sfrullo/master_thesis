# coding: utf-8

# native
import os

# external
import xmltodict
import numpy as np

# custom
from dataset import dataset

from dataset.mahnob import config
from dataset.mahnob.session import Session

class Mahnob(dataset.Dataset):

    def __init__(self):

        # contains all the sessions instances
        self.sessions = {}
        self.__load_sessions()

    def __load_sessions(self):
        sessions = []
        for root, dirs, files in os.walk(config.DIR_MAHNOB['Sessions']):
            if files:
                session_file_path = os.path.join(root, "session.xml")
                with open(session_file_path) as f:
                    xml = f.read()
                    session_data = xmltodict.parse(xml)
                    session = Session(session_data, root_path=root)
                    sessions.append(session)
        self.sessions = { int(s.get_sessionId()) : s for s in sessions }

    def __get_session_by_id(self, sid):
        try:
            return self.sessions[sid]
        except KeyError as e:
            print "Session #{} not available".format(sid)
            raise e

    def get_session_by_id(self, sids=[]):
        sessions = {}
        if not isinstance(sids, list):
            sids = [sids]
        for sid in sids:
            sessions[sid] = self.__get_session_by_id(sid)
        return sessions

    def get_sessions_by_mediafile(self, mediaFiles=[]):
        if not isinstance(mediaFiles, list):
            mediaFiles = [mediaFiles]
        return { sid : session for sid, session in self.sessions.items() if session.get_mediaFile() in mediaFiles }

    def collect_gaze_data(self, sessions=None, mapped=False, remove_blink=True):

        if sessions is None:
            raise ValueError("Must give a list of sessions.")

        coordinates_data = []
        fixations_data = []

        for sid, session in sessions.items():
            gd = session.get_gaze_data()
            coordinates = gd.get_gaze_coordinates(mapped=mapped, remove_blink=remove_blink)
            coordinates_data.append(coordinates)

            fixations = gd.get_fixations_data()
            fixations_data.append(fixations)

        coordinates, fixations = np.array(zip(*coordinates_data)), np.array(zip(*fixations_data))

        gaze_data = {
            "coordinates" : coordinates,
            "fixations" : fixations
        }

        return gaze_data

if __name__ == '__main__':

    mahnob = Mahnob()
    print mahnob.get_session_by_id(10)

    for sid, session in mahnob.get_session_by_id(10).items():
        print "mediaFile =", session.get_mediaFile()
        tracks = session.get_tracks()
        for t in tracks:
            print "\t", t.get_type(), t.get_filename()
            for a in t.get_annotations():
                print "\t\t", a.get_type(), a.get_filename()

    for sid, session in mahnob.get_session_by_id(10).iteritems():
        gd = session.get_gaze_data()
        print len(gd.data)
        print gd.get_gaze_coordinates()
        print gd.get_gaze_coordinates(mapped=True)
        print gd.get_fixations_coordinates()

    print mahnob.get_sessions_by_mediafile("53.avi")