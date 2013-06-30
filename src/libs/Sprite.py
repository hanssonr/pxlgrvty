import pygame, libs.pygl2d as gl
from libs.Pgl import *

class Sprite(object):
    
    def __init__(self, image):
        self.originalImage = image
        self.image = image
        self.pos = image.get_rect()
        self.mFlippedX, self.mFlippedY = False, False
        
    def draw(self):
        Pgl.app.surface.blit(self.image, self.pos)
    
    def setSize(self, width, height):
        self.image = pygame.transform.scale(self.image, (width, height))
        self.originalImage = self.image
    
    def setPosition(self, x, y):
        self.pos = (x, y)
    
    def flip(self, xbool, ybool):
        self.mFlippedX = xbool
        self.mFlippedY = ybool
        self.image = pygame.transform.flip(self.originalImage, xbool, ybool)
        
    def flippedX(self):
        return self.mFlippedX
    
    def flippedY(self):
        return self.mFlippedY
    
    
    
    