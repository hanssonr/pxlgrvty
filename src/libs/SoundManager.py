from Resources import Resources
from Pgl import *
import random, pygame

class SoundManager(object):
    
    INSTANCE = None
    VOLUME = 0.3
    SOUNDS = None
    MUSIC = None
    MUSIC_PLAYING = None
    
    def __init__(self):
        if self.INSTANCE is not None:
            raise ValueError("already instantiated")
        
    def initialize(self):
        self.SOUNDS = [Resources.getInstance().mJump, 
                       Resources.getInstance().mFleshExplosion]
        self.MUSIC_PLAYING = -1
    
    
    def playMusic(self, musicId):
        if self.MUSIC_PLAYING == musicId: return
        if Pgl.options.music:
            song = ""
            if musicId == MusicID.BG:
                #song = "bg%s" % str(random.randrange(1, 3))
                song = "bg1"
                self.MUSIC_PLAYING = MusicID.BG
            elif musicId == MusicID.MENU:
                song = "bg1"
                self.MUSIC_PLAYING = MusicID.MENU
            
            pygame.mixer.music.set_volume(self.VOLUME)
            pygame.mixer.music.load("assets/audio/music/%s.ogg" % song)
            pygame.mixer.music.play(-1)
            print "PLAY MUSIC %s" % song
        else:
            self.stopMusic()
    
    def pauseMusic(self):
        pass
    
    def stopMusic(self):
        pygame.mixer.music.stop()
     
    def playSound(self, soundId):
        if Pgl.options.sound:
            sound = self.SOUNDS[soundId]
            
            sound.set_volume(self.VOLUME)
            sound.play()
    
    @classmethod
    def getInstance(cls):
        if cls.INSTANCE is None:
            cls.INSTANCE = SoundManager()
        return cls.INSTANCE
    

class SoundID:
    JUMP = 0
    FLESHEXPLOSION = 1
    
class MusicID:
    MENU = 0
    BG = 1
    
    