# coding: utf-8

# native
import os, sys
sys.path.append(os.path.dirname(__file__) + "/..")

# external
import xmltodict

# custom
from dataset import dataset
from signaldata import signal

#
# MAHNOB DIRECTORIES
#

DIR_BASE = '/media/sf_vbfolder/TesiCastellani/Dataset/Mahnob'
DIR_MAHNOB = {
    'MediaFiles' : os.path.join(DIR_BASE, 'data/MediaFiles'),
    'Sessions' : os.path.join(DIR_BASE, 'data/Sessions'),
    'Subjects' : os.path.join(DIR_BASE, 'data/Subjects'),
}

class Base(object):
    """docstring for Base"""
    def __init__(self, attributes):
        self.__metadata = attributes
        for k in self.__metadata.keys():
            if k.startswith('@'):
                setattr(self, "get_" + k[1:], self.__get_metadata_wrapper(k))

    def __get_metadata_wrapper(self, key):
        def get_metadata():
            return self.__metadata[key]
        return get_metadata

class Track(Base):
    """docstring for Track"""
    def __init__(self, track):
        Base.__init__(self, track)

        self.__annotations = []

        annotations = track['annotation']
        # fix case with one annotation which is not grouped in a list
        if not isinstance(annotations, list):
            annotations = [annotations]
        for annotation in annotations:
            self.__annotations.append(Annotation(annotation))

    def get_annotations(self, annotation_type=None):
        if annotation_type is None:
            return self.__annotations
        annotations = [ a for a in self.__annotations if a.get_type() == annotation_type ]
        return annotations

class Annotation(Base):
    """docstring for Annotation"""
    def __init__(self, annotation):
        Base.__init__(self, annotation)

class Subject(Base):
    """docstring for Annotation"""
    def __init__(self, subject):
        Base.__init__(self, subject)

class Session(Base):

    def __init__(self, session_data, root_path):

        self.root_path = root_path

        session = session_data["session"]
        Base.__init__(self, session)

        subject = session['subject']
        self.__subject = Subject(subject)

        tracks = session['track']
        self.__tracks = []
        for track in tracks:
            self.__tracks.append(Track(track))

    def get_subject(self):
        return self.__subject

    def get_tracks(self, track_type=None):
        if track_type is None:
            return self.__tracks
        tracks = [ t for t in self.__tracks if t.get_type() == track_type ]
        return tracks

    def __get_physiological_data(self):
        tracks = self.get_tracks(track_type='Physiological')[0]
        return tracks

    def get_gaze_data(self):
        tracks = self.get_tracks(track_type='Video')[0]
        annotation = tracks.get_annotations(annotation_type='Gaze')
        return signal.GazeData(annotation)

    def get_eeg_data(self):
        track = self.__get_physiological_data()
        return signal.EEGData(track)

    def get_ecg_data(self):
        track = self.__get_physiological_data()
        return signal.ECGData(track)

    def get_gsr_data(self):
        track = self.__get_physiological_data()
        return signal.GSRData(track)

    def get_resp_data(self):
        track = self.__get_physiological_data()
        return signal.RespData(track)

    def get_temperature_data(self):
        track = self.__get_physiological_data()
        return signal.TemperatureData(track)

    def get_status_channel(self):
        track = self.__get_physiological_data()
        return signal.StatusData(track)


class Mahnob(dataset.Dataset):

    def __init__(self):

        # contains all the sessions instances
        self.sessions = {}
        self.__load_sessions()

    def __load_sessions(self):
        sessions = []
        for root, dirs, files in os.walk(DIR_MAHNOB['Sessions']):
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
        print session.get_gaze_data()
        print session.get_physiological_data()

    print mahnob.get_sessions_by_mediafile("53.avi")