__author__ = 'zelgadis'

import os.path

class RenderChanProjectManager():
    def __init__(self):
        self.list = {}

    def load(self, path):
        confFile = os.path.join(path,"project.conf")
        if not os.path.exists(confFile):
            # Look for remake.conf
            confFile = os.path.join(path,"remake.conf")
        if not os.path.exists(confFile):
            raise Exception

        # TODO: Load project cache here
        # ...

        self.list[path]=RenderChanProject(confFile)

    def get(self, path):
        if not self.list.has_key(path):
            self.load(path)

        return self.list[path]

class RenderChanProject():
    def __init__(self, confFile):
        pass

    def getFormat(self):
        # FIXME: Get format from project configuration
        return "png"