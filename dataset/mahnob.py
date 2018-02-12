# coding: utf-8

# native
import os
import pprint as pprint

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


class Session(object):

    def __init__(self, root_path):
        self.root_path = root_path
        self.session_file_path = os.path.join(self.root_path, "session.xml")

        self.session = {}
        self.subject = {}
        self.tracks = []
        self.annotations = []

        with open(self.session_file_path) as f:
            xml = f.read()
            data = xmltodict.parse(xml)
            session = data['session']
            subject = session['subject']
            tracks = session['track']
            self.session = { k[1:]:v for k,v in session.items() if k.startswith('@') }
            self.subject = { k[1:]:v for k,v in subject.items() if k.startswith('@') }
            self.tracks = tracks

        print self.session
        print self.subject
        print self.tracks

class Mahnob(dataset.Dataset):

    def __init__(self):

        # contains all the sessions instances
        self.sessions = {}
        self.load_sessions()

    def load_sessions(self):
        sessions = []
        for root, dirs, files in os.walk(DIR_MAHNOB['Sessions']):
            if files:
                sessions.append(Session(root))
                break
        self.sessions = { s.get_id() : s for s in sessions }


if __name__ == '__main__':

    mahnob = Mahnob()