__author__ = 'Konstantin Dmitriev'

from renderchan.module import RenderChanModule
import subprocess
import random
import os
import tempfile
from zipfile import ZipFile
from xml.etree import ElementTree
from renderchan.utils import which
from renderchan.utils import mkdirs

class RenderChanKritaModule(RenderChanModule):
    def __init__(self):
        RenderChanModule.__init__(self)
        if os.name == 'nt':
            self.conf['convert_binary']=os.path.join(os.path.dirname(__file__),"..\\..\\..\\imagemagick\\bin\\convert.exe")
            self.conf['binary']=os.path.join(os.path.dirname(__file__),"..\\..\\..\\krita\\bin\\krita.exe")
        else:
            #TODO: Additional bunaries should be separate modules
            self.conf['convert_binary']="convert"
            self.conf['binary']="krita"

        self.conf["packetSize"]=0

        self.extraParams['use_own_dimensions']='1'
        self.extraParams['proxy_scale']='1.0'

    def getInputFormats(self):
        return ["kra"]

    def getOutputFormats(self):
        return ["png"]

    def checkRequirements(self):
        if which(self.conf['binary']) == None:
            self.active=False
            print("Module warning (%s): Cannot find '%s' executable." % (self.getName(), self.conf['binary']))
            print("    Please install krita package.")
            return False
        if which(self.conf['convert_binary']) == None:
            self.active=False
            print("Module warning (%s): Cannot find '%s' executable!" % (self.getName(), self.conf['convert_binary']))
            print("    Please install ImageMagick package.")
            return False
        self.active=True
        return True

    def analyze(self, filename):
        info={'dependencies':[], 'width':0, 'height':0}
        
        with tempfile.TemporaryDirectory() as tmpPath:
            with ZipFile(filename) as zip:
                mdPath = zip.extract('maindoc.xml', tmpPath)
            
            with open(mdPath, "rb") as f:
                #TODO: Consider file layers as dependencies
                #...
                
                tree = ElementTree.parse(f)
                root = tree.getroot()

                # Extracting width/height
                info["width"] = root.find("{http://www.calligra.org/DTD/krita}IMAGE").attrib["width"]
                info["height"] = root.find("{http://www.calligra.org/DTD/krita}IMAGE").attrib["height"]

        return info

    def render(self, filename, outputPath, startFrame, endFrame, format, updateCompletion, extraParams={}):

        comp = 0.0
        updateCompletion(comp)

        deps_count=0
        for item in extraParams["dependencies"]:
            if not item.endswith(".conf"):
                deps_count+=1
                break

        with tempfile.TemporaryDirectory() as tmpPath:
            outputPathTmp = os.path.join(tmpPath, "image." + format)
            if deps_count==0:
                with ZipFile(filename) as zip:
                    zip.extract('mergedimage.png', tmpPath)
                #TODO: Compress image?
                os.rename(os.path.join(tmpPath,"mergedimage.png"), outputPathTmp)
            else:
                #TODO: PNG transperency settings at ~/.kde/share/config/kritarc ? use KDEHOME env ?
                commandline=[self.conf['binary'], "--export", filename, "--export-filename", outputPathTmp]
                subprocess.check_call(commandline)

            dimensions = extraParams["width"]+"x"+extraParams["height"]
            commandline=[self.conf['convert_binary'], outputPathTmp, "-resize", dimensions, outputPath]
            subprocess.check_call(commandline)

        updateCompletion(1)
