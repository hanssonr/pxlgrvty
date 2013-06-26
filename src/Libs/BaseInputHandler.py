import pygame
from pygame.locals import *
from Libs.Pgl import *

class BaseInputHandler(object):
    
    def update(self):
        for event in pygame.event.get():
            self.checkEvent(event)
    
    def checkEvent(self, event):
        if event.type == pygame.QUIT:
            Pgl.app.stop()
        