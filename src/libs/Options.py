import json

class Options(object):
    
    __mResolution = None
    __mMusic = None
    __mSound = None
    __mFullscreen = None
    __mSoundVolume = None
    __mMusicVolume = None
    
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
                json.dump({"FULLSCREEN": False, "MUSIC": True, "SOUND": True, "RESOLUTION":"640x480", "MUSICVOLUME":"30", "SOUNDVOLUME":"30"}, writestate)
            
        finally:
            with open("assets/state/options.json", "r") as readstate:
                optionData = json.load(readstate)
        
        self.__mFullscreen = optionData[OptionValue.FULLSCREEN]
        self.__mMusic = optionData[OptionValue.MUSIC]
        self.__mSound = optionData[OptionValue.SOUND]
        self.__mResolution = optionData[OptionValue.RESOLUTION]
        self.__mMusicVolume = optionData[OptionValue.MUSICVOLUME]
        self.__mSoundVolume = optionData[OptionValue.SOUNDVOLUME]
        
    def writeOptions(self):
        try:
            with open(self.__optionPath, "w+") as writestate:
                json.dump({"FULLSCREEN": self.fullscreen, 
                           "MUSIC": self.music,
                           "SOUND": self.sound,
                           "RESOLUTION": self.resolution,
                           "SOUNDVOLUME": self.soundvolume,
                           "MUSICVOLUME": self.musicvolume}, writestate)      
        except:
            print "WriteError"
    
    def setDefaultOptions(self):
        self.__mFullscreen = False
        self.__mMusic = True
        self.__mSound = True
        self.__mResolution = "640x480"
    
    def getResolutionAsList(self):
        return [int(x) for x in self.__mResolution.replace("x", " ").split(" ")]

    def __getFullscreen(self):
        return self.__mFullscreen
    
    def __setFullscreen(self, boolean):
        self.__mFullscreen = boolean
    
    def __getMusic(self):
        return self.__mMusic
    
    def __setMusic(self, boolean):
        self.__mMusic = boolean
        
    def __getSound(self):
        return self.__mSound
    
    def __setSound(self, boolean):
        self.__mSound = boolean
        
    def __getResolution(self):
        return self.__mResolution
    
    def __setResolution(self, res):
        self.__mResolution = res
        
    def __getMusicVolume(self):
        return int(self.__mMusicVolume)
    
    def __setMusicVolume(self, volume):
        self.__mMusicVolume = int(volume)
    
    def __getSoundVolume(self):
        return int(self.__mSoundVolume)
    
    def __setSoundVolume(self, volume):
        self.__mSoundVolume = int(volume)
    
    fullscreen = property(__getFullscreen, __setFullscreen)
    music = property(__getMusic, __setMusic)
    sound = property(__getSound, __setSound)
    resolution = property(__getResolution, __setResolution)
    soundvolume = property(__getSoundVolume, __setSoundVolume)
    musicvolume = property(__getMusicVolume, __setMusicVolume)

class OptionValue(object):
    FULLSCREEN = "FULLSCREEN"
    MUSIC = "MUSIC"
    SOUND = "SOUND"
    RESOLUTION = "RESOLUTION"
    MUSICVOLUME = "MUSICVOLUME"
    SOUNDVOLUME = "SOUNDVOLUME"
        