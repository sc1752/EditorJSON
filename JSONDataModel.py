import json
from json.decoder import JSONDecodeError

Sample_JSON = "{\n\"Message\": \"Welcome to JSON Editor\",\n\"Description\": \"Simple JSON viewer/editor for editing and viewing JSON text files.\",\n\"Edit Mode\": [\"Text View\", \"Tree View\"],\n\"About\": {\n\t\"Year\": 2021,\n\t\"Readme\" : \"https://github.com/sc1752/EditorJSON/wiki\"\n\t }\n}"

class JSONDataModel():

    def __init__(self):
        self.JSONdata = None
        self.Text = None
        self.File = None

        self.NewFile()

    def NewFile(self):
        self.Text = Sample_JSON
        self.JSONdata = None
        self.SyncTextToData()

    def ValidateJSONText(self):
        """Returns None if JSON text data is valid using JSON module.""" 
        try: 
            json.loads(self.Text)
        except JSONDecodeError as err:
            raise err

    def ValidateJSONData(self):
        """Returns None if JSON data dict is valid using JSON module.""" 
        try: 
            json.dumps(self.JSONdata)
        except ValueError as err:
            raise err

    def SyncDataToText(self):
        """Syncs JSON data to Text"""
        try:
            self.Text = json.dumps(self.JSONdata, indent=4)
        except ValueError as err:
            raise err

    def SyncTextToData(self):
        """Syncs Text to data"""
        try:
            data = json.loads(self.Text)
            if data != self.JSONdata:
                self.JSONdata = data
        except JSONDecodeError as err:
            raise err
    
    def SetJSONText(self, text):
        """Set JSON Text Data"""
        self.Text = text

    def SetJSONData(self, data):
        self.JSONdata = data

    def PrettifyText(self):

        self.SyncTextToData()
        self.Text = json.dumps(self.JSONdata, indent=4)
        

    def CompactifyText(self):

        self.SyncTextToData()
        self.Text = json.dumps(self.JSONdata, separators=(",", ":"))
        