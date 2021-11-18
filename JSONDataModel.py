import json
from json.decoder import JSONDecodeError
import time

Sample_JSON = "{\n\t\"Message\": \"Welcome to JSON Editor\",\n\t\"Year\": 2021,\n\t\"Array\": [\"apple\", \"orange\"],\n\t\"Object\": {\n\t\t\"ID\": 1,\n\t\t\"Name\" : \"Object\"\n\t }\n}"

class JSONDataModel():

    def __init__(self):
        self.JSONdata = None
        self.Text = None
        self.File = None

        self.NewFile()

    def NewFile(self):
        self.Text = Sample_JSON
        
        self.LastModifiedTime = time.time()
        self.LastSavedTime = time.time()

    def IsDocumentSaved(self):
        return self.LastSavedTime >= self.LastSavedTime

    def ValidateJSONText(self):
        """Returns None if JSON text data is valid using JSON module.""" 
        try: 
            json.loads(self.Text)
        except JSONDecodeError:
            return False
        return True


    def ValidateJSONData(self):
        """Returns None if JSON data dict is valid using JSON module.""" 
        try: 
            json.dumps(self.JSONdata)
        except ValueError:
            return False
        return True

    def SyncDataToText(self):
        """Syncs JSON data to Text"""
        try:
            self.Text = json.dumps(self.JSONdata, indent=4)
        except ValueError as err:
            raise err

    def SyncTextToData(self):
        """Syncs Text to data"""
        try:
            self.JSONdata = json.loads(self.Text)
        except JSONDecodeError as err:
            raise err
    
    def SetJSONText(self, text):
        """Set JSON Text Data"""
        self.Text = text

    def SetJSONData(self, data):
        self.JSONdata = data
