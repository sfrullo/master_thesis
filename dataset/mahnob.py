# coding: utf-8

# native
import os

# external
import xmltodict
import untangle

# custom
import dataset

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
        for k, v in attributes.items():
            if k.startswith('@'):
                setattr(self, k[1:], v)

class Track(Base):
    """docstring for Track"""
    def __init__(self, track):
        Base.__init__(self, track)

        self.annotations = []

        annotations = track['annotation']
        # fix case with one annotation which is not grouped in a list
        if not isinstance(annotations, list):
            annotations = [annotations]
        for annotation in annotations:
            self.annotations.append(Annotation(annotation))

    def get_all_annotations(self):
        return self.annotations

class Annotation(Base):
    """docstring for Annotation"""
    def __init__(self, annotation):
        Base.__init__(self, annotation)

class Subject(Base):
    """docstring for Annotation"""
    def __init__(self, subject):
        Base.__init__(self, subject)

class Session(object):

    def __init__(self, root_path):
        self.root_path = root_path
        self.session_file_path = os.path.join(self.root_path, "session.xml")

        self._metadata = {}

        self.__subject = None
        self.__tracks = []

        with open(self.session_file_path) as f:
            xml = f.read()
            data = xmltodict.parse(xml)
            session = data['session']
            self._metadata = { k:v for k,v in session.items() if k.startswith('@') }

            subject = session['subject']
            self.__subject = Subject(subject)

            tracks = session['track']
            for track in tracks:
                self.__tracks.append(Track(track))

        # setup metadata getter
        for key in self._metadata:
            setattr(self, "get_" + key[1:], self.__get_metadata_wrapper(key))

    def __get_metadata_wrapper(self, key):
        def get_metadata():
            return self._metadata[key]
        return get_metadata

    def get_subject(self):
        return self.__subject

    def get_tracks(self):
        return self.__tracks

class Mahnob(dataset.Dataset):

    def __init__(self):

        # contains all the sessions instances
        self.sessions = {}
        self.__load_sessions()

    def __load_sessions(self):
        sessions = []
        for root, dirs, files in os.walk(DIR_MAHNOB['Sessions']):
            if files:
                sessions.append(Session(root))
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
    print mahnob.get_sessions_by_mediafile("53.avi")