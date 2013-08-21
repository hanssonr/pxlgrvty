"""
Optionclass handles the optionfile and read/writes new parameters to it

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

import json

class Options(object):
    
    __mResolution = None
    __mMusic = None
    __mSound = None
    __mFullscreen = None
    __mSoundVolume = None
    __mMusicVolume = None
    __mUpdaterate = None
    
    __optionPath = "assets/state/options.json"
    
    def __init__(self):
        self.readOptions()
    
    def readOptions(self):
        optionData = None
        
        try:
            with open(self.__optionPath, "r") as readstate:
                optionData = json.load(readstate)
        except (IOError, ValueError):
            with open(self.__optionPath, "w+") as writestate:
                json.dump({"FULLSCREEN": False, "MUSIC": True, "SOUND": True, "RESOLUTION":"640x480", "MUSICVOLUME":"30", "SOUNDVOLUME":"30", "UPDATERATE":"60"}, writestate)
            
        finally:
            with open("assets/state/options.json", "r") as readstate:
                optionData = json.load(readstate)
        
        self.__mFullscreen = optionData[OptionValue.FULLSCREEN]
        self.__mMusic = optionData[OptionValue.MUSIC]
        self.__mSound = optionData[OptionValue.SOUND]
        self.__mResolution = optionData[OptionValue.RESOLUTION]
        self.__mMusicVolume = optionData[OptionValue.MUSICVOLUME]
        self.__mSoundVolume = optionData[OptionValue.SOUNDVOLUME]
        self.__mUpdaterate = int(optionData[OptionValue.UPDATERATE])
        
    def writeOptions(self):
        try:
            with open(self.__optionPath, "w+") as writestate:
                json.dump({"FULLSCREEN": self.fullscreen, 
                           "MUSIC": self.music,
                           "SOUND": self.sound,
                           "RESOLUTION": self.resolution,
                           "SOUNDVOLUME": self.soundvolume,
                           "MUSICVOLUME": self.musicvolume,
                           "UPDATERATE": self.updaterate}, writestate)      
        except:
            print "WriteError"
    
    def setDefaultOptions(self):
        self.__mFullscreen = False
        self.__mMusic = True
        self.__mSound = True
        self.__mResolution = "640x480"
        self.__mUpdaterate = 60
    
    def getResolutionAsList(self):
        return [int(x) for x in self.__mResolution.replace("x", " ").split(" ")]

    def getFullscreen(self):
        return self.__mFullscreen
    
    def setFullscreen(self, boolean):
        self.__mFullscreen = boolean
    
    def getMusic(self):
        return self.__mMusic
    
    def setMusic(self, boolean):
        self.__mMusic = boolean
        
    def getSound(self):
        return self.__mSound
    
    def setSound(self, boolean):
        self.__mSound = boolean
        
    def getResolution(self):
        return self.__mResolution
    
    def setResolution(self, res):
        self.__mResolution = res
        
    def getMusicVolume(self):
        return int(self.__mMusicVolume)
    
    def setMusicVolume(self, volume):
        self.__mMusicVolume = int(volume)
    
    def getSoundVolume(self):
        return int(self.__mSoundVolume)
    
    def setSoundVolume(self, volume):
        self.__mSoundVolume = int(volume)

    def getUpdaterate(self):
        return int(self.__mUpdaterate)
        
    def setUpdaterate(self, updaterate):
        self.__mUpdaterate = updaterate

    fullscreen = property(getFullscreen, setFullscreen)
    music = property(getMusic, setMusic)
    sound = property(getSound, setSound)
    resolution = property(getResolution, setResolution)
    soundvolume = property(getSoundVolume, setSoundVolume)
    musicvolume = property(getMusicVolume, setMusicVolume)
    updaterate = property(getUpdaterate, setUpdaterate)

class OptionValue(object):
    FULLSCREEN = "FULLSCREEN"
    MUSIC = "MUSIC"
    SOUND = "SOUND"
    RESOLUTION = "RESOLUTION"
    MUSICVOLUME = "MUSICVOLUME"
    SOUNDVOLUME = "SOUNDVOLUME"
    UPDATERATE = "UPDATERATE"
    
class Updaterate(object):
    SLOW = "30"
    MEDIUM = "45"
    FAST = "60"
    
    @staticmethod
    def convertIntToSpeed(x):
        if x == 0:
            return Updaterate.SLOW
        elif x == 1:
            return Updaterate.MEDIUM
        elif x == 2:
            return Updaterate.FAST
        else:
            raise Exception("No such Updaterate")
        
    @staticmethod
    def convertSpeedToInt(speed):
        speed = int(speed)
        if speed == int(Updaterate.SLOW):
            return 0
        elif speed == int(Updaterate.MEDIUM):
            return 1
        elif speed == int(Updaterate.FAST):
            return 2
        else:
            raise Exception("No such Updaterate")
        