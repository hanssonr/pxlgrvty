from Resources import Resources
from Pgl import *
import random, pygame

class SoundManager(object):
    
    INSTANCE = None
    SOUNDS = None
    MUSIC = None
    MUSIC_PLAYING = None
    CURRENTSONG = 0
    
    def __init__(self):
        if self.INSTANCE is not None:
            raise ValueError("already instantiated")
        
    def initialize(self):
        self.SOUNDS = [Resources.getInstance().mJump, 
                       Resources.getInstance().mFleshExplosion]
        self.MUSIC_PLAYING = -1
    
    
    def playMusic(self, seed = 0):
        if Pgl.options.music:
            print seed, self.CURRENTSONG
            seed = 1 if seed > 3 else seed
            song = "bg%s" % str(seed)
            self.MUSIC_PLAYING = MusicID.BG
            self.CURRENTSONG = seed
            
            pygame.mixer.music.set_volume(Pgl.options.musicvolume / 100.0)
            pygame.mixer.music.load("assets/audio/music/%s.ogg" % song)
            pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
            pygame.event.set_allowed(pygame.constants.USEREVENT)
            pygame.mixer.music.play()
            
        else:
            self.stopMusic()
            
    def playMenuMusic(self):
        if Pgl.options.music:
            if self.MUSIC_PLAYING == MusicID.MENU: return
            pygame.mixer.music.set_volume(int(Pgl.options.musicvolume) / 100.0)
            pygame.mixer.music.load("assets/audio/music/menu.ogg")
            pygame.mixer.music.play(-1)
            self.MUSIC_PLAYING = MusicID.MENU
            
    def changeMusicVolume(self):
        pygame.mixer.music.set_volume(Pgl.options.musicvolume / 100.0)
    
    def pauseMusic(self, pause):
        if pause:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
    
    def stopMusic(self):
        self.MUSIC_PLAYING = -1
        pygame.mixer.music.stop()
     
    def playSound(self, soundId):
        if Pgl.options.sound:
            sound = self.SOUNDS[soundId]
            
            sound.set_volume(Pgl.options.soundvolume / 100.0)
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
    
    