import pygame
from pygame.locals import *
from libs.BaseInputHandler import BaseInputHandler

class MenuInput(BaseInputHandler):
    
    def __init__(self, screen):
        self.mLevelScreen = screen
    
    def update(self):  
        e = pygame.event.poll()      
        
        BaseInputHandler.checkEvent(self, e)
        
        
        self.mLevelScreen.mouseOver(pygame.mouse.get_pos())
        
        if e.type == MOUSEBUTTONDOWN:
            print e.button
            if e.button == 1:
                self.mLevelScreen.mouseClick(e.pos)