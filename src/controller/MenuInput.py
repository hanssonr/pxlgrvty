import pygame
from pygame.locals import *
from libs.BaseInputHandler import BaseInputHandler

class MenuInput(BaseInputHandler):
    
    def __init__(self, screen):
        self.mMenuScreen = screen
    
    def update(self):  
        e = pygame.event.poll()      
        
        BaseInputHandler.checkEvent(self, e)
        
        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                self.mMenuScreen.mouseClick(e.pos)
                
    def getMousePosition(self):
        return pygame.mouse.get_pos()