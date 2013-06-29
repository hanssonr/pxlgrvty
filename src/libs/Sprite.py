import pygame, libs.pygl2d as gl
from libs.Pgl import *

class Sprite(object):
    
    def __init__(self, image):
        self.image = image
        self.pos = image.get_rect()
        
    def draw(self):
        Pgl.app.surface.blit(self.image, self.pos)
    
    def setSize(self, width, height):
        self.image = pygame.transform.scale(self.image, (width, height))
    
    def setPosition(self, x, y):
        self.pos = (x, y)
    
    
    
    