# EruditeScience Sample API for PyCon 2015
# Written in 2015 by Erudite Science <contact@eruditescience.com>

#    To the extent possible under law, the author(s) have dedicated
#    all copyright and related and neighboring rights to this software
#    to the public domain worldwide. This software is distributed
#    without any warranty.

#    You should have received a copy of the CC0 Public Domain
#    Dedication along with this software. If not, see
#    <http://creativecommons.org/publicdomain/zero/1.0/>.

try:
    import requests
except:
    assert False, "Please install the requirements: pip install -r requirements.txt"
    
import json

HOST = "http://pycon2015.eruditescience.com/api"
    
ENDPOINTS = {
    "CREATE_SESSION_PATH": '/session/new',
    "NEXT_STEP_PATH": '/step'
}

class Sphinx(object):

    def __init__(self, language='en', medium='plain'):
        """
        Create an Sphinx object, languages available in this demo: English (en), French (fr), Spanish (es).
        Media available are plain text (plain), text with colors (color) and spoken output (speech).
        """
        self.language = language
        self.medium = medium
        print "This is a limited demo of EruditeScience Sphinx API for PyCon 2015, enjoy it!"

    def create_session(self, formula=None, level=4):
        
        params = { 'level': level }
        if formula is not None:
            params['formula'] = formula
        request = requests.get(HOST + ENDPOINTS["CREATE_SESSION_PATH"], params=params)
        request_json = json.loads(request.content)
        return Session(request_json['formula'], request_json['session_id'], self.language, self.medium)

class Session(object):

    def __init__(self, formula, session_id, language, medium):
        self.formula = formula
        self.session_id = session_id
        self.language = language
        self.medium = medium

    def next_step(self, formula):
        params = {'formula': formula}
        url = HOST + ENDPOINTS['NEXT_STEP_PATH'] + '/' + str(self.session_id)
        request = requests.post(url, data=params)
        request_json = json.loads(request.content)
        self.feedback = request_json['text'][self.language][self.medium]['text']
        self.finished = request_json['finished']
        self.in_error = request_json['in_error']
        self.correct = request_json['correct']
