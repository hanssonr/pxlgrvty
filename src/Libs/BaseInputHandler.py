import pygame, random
from pygame.locals import *
from libs.Pgl import *
from SoundManager import SoundManager, MusicID

class BaseInputHandler(object):
    
    def update(self):
        for event in pygame.event.get():
            self.checkEvent(event)
    
    def checkEvent(self, event):
        if event.type == pygame.QUIT:
            Pgl.app.stop()
        elif event.type == pygame.USEREVENT:
            SoundManager.getInstance().stopMusic()
            SoundManager.getInstance().playMusic(SoundManager.getInstance().CURRENTSONG+1)
            
        