__author__ = 'Konstantin Dmitriev'

from renderchan.module import RenderChanModule
from renderchan.utils import is_true_string
import subprocess
import gzip
import os, sys
import errno
import re
from xml.etree import ElementTree

class RenderChanListModule(RenderChanModule):
    def __init__(self):
        RenderChanModule.__init__(self)
        if os.name == 'nt':
            self.conf['binary']=os.path.join(os.path.dirname(__file__),"..\\..\\..\\ffmpeg\\bin\\ffmpeg.exe")
        else:
            self.conf['binary']="ffmpeg"
        self.conf["packetSize"]=100
        self.conf["maxNbCores"]=1

        # Extra params
        self.extraParams["single"]="None"
        self.extraParams["extract_alpha"]="0"

    def getInputFormats(self):
        return ["lst"]

    def getOutputFormats(self):
        return []

    def analyze(self, filename):

        info={ "dependencies":[], "width": 0, "height": 0 }

        dir = os.path.dirname(filename)

        f=open(filename, 'r')
        for i,line in enumerate(f.readlines()):
            if i==0 and line.startswith("FPS "):
                pass
            else:
                info["dependencies"].append(os.path.join(dir,line.strip()))
        f.close()

        return info

    def render(self, filename, outputPath, startFrame, endFrame, format, updateCompletion, extraParams={}):

        comp = 0.0
        updateCompletion(comp)


        print('================================================================')
        print('WARNING:  No rendering available for lst files yet. Skipping.')
        print('================================================================')

        updateCompletion(1)
