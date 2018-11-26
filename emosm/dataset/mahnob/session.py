# coding: utf-8

# native
import os

# external
import xmltodict

# custom
from emosm.dataset.mahnob import config
from emosm.dataset import media
from emosm.dataset.mahnob.signals import gaze, eda, resp, ecg, skt

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

    __media = {}

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

    def get_session_info(self):

        session_info = {
            "sessionId" : self.get_sessionId(),
            "date" : self.get_date(),
            "time" : self.get_time(),
            "experimentType" : self.get_experimentType(),
            "isStim" : self.get_isStim(),
            "feltEmo" : self.get_feltEmo(),
            "feltArsl" : self.get_feltArsl(),
            "feltVlnc" : self.get_feltVlnc(),
            "feltCtrl" : self.get_feltCtrl(),
            "feltPred" : self.get_feltPred(),
            "cutNr" : self.get_cutNr(),
            "cutLenSec" : self.get_cutLenSec(),
            "vidRate" : self.get_vidRate(),
            "audRate" : self.get_audRate(),
            "audBeginSmp" : self.get_audBeginSmp(),
            "audEndSmp" : self.get_audEndSmp(),
            "vidBeginSmp" : self.get_vidBeginSmp(),
            "vidEndSmp" : self.get_vidEndSmp(),
            "mediaFile" : self.get_mediaFile(),
        }

        return session_info

    def get_real_path(self, filename):
        path = os.path.join(self.root_path, filename)
        return os.path.realpath(path)

    def get_media(self):
        mediafile = self.get_mediaFile()
        if mediafile not in self.__media:
            filename = os.path.join(config.DIR_MAHNOB["MediaFiles"], mediafile)
            self.__media[mediafile] = media.Media(filename=filename)
        return self.__media[mediafile]

    def get_subject(self):
        return self.__subject

    def get_tracks(self, track_type=None):
        if track_type is None:
            return self.__tracks
        tracks = [ t for t in self.__tracks if t.get_type() == track_type ]
        return tracks

    def get_physiological_data(self, signals=()):

        sigCls = {
            "ECG" : ecg.ECGData,
            "EDA" : eda.EDAData,
            "Resp" : resp.RespData,
            "SKT": skt.SKTData
        }

        try:
            track = self.get_tracks(track_type='Physiological')[0]
        except IndexError:
            print "Missing physiological data for session #{}".format(self.get_sessionId())
            return {}

        filename = self.get_real_path(track.get_filename())

        physio_data = {}
        for signal in signals:
            physio_data[signal] = sigCls[signal](filename=filename)

        return physio_data

    def get_gaze_data(self):
        tracks = self.get_tracks(track_type='Video')[0]
        annotation = tracks.get_annotations(annotation_type='Gaze')[0]
        filename = self.get_real_path(annotation.get_filename())
        return gaze.GazeData(filename=filename)