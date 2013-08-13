import pygame
from Box2D import b2Vec2, b2Vec2_zero
from libs.Pgl import *

class Sprite(object):
    
    __mFlippedX = False
    __mFlippedY = False
    __mRotation = 0
    __mSize = None

    
    def __init__(self, image, size = b2Vec2_zero):
        self.image = image
        self.pos = image.get_rect()
        self.__mSize = size
        
    def draw(self, pos = None, area = None):
        toDraw = self.image
        
        if area != None:
            toDraw = self.image.subsurface(area)
            toDraw = pygame.transform.flip(toDraw, self.__mFlippedX, self.__mFlippedY)
            toDraw = pygame.transform.rotate(toDraw, self.__mRotation)

        if self.__mSize != b2Vec2_zero:
            toDraw = pygame.transform.scale(toDraw, (int(self.__mSize.x), int(self.__mSize.y)))
        
        if pos != None:
            Pgl.app.surface.blit(toDraw, pos)
        else:
            Pgl.app.surface.blit(toDraw, self.pos)
    
    def setSize(self, size):
        self.__mSize = size
    
    def getSize(self):
        return self.__mSize
    
    def setPosition(self, x, y):
        self.pos = (x,y)
        
    def flipX(self):
        self.__mFlippedX = not self.__mFlippedX
    
    def flipY(self):
        self.__mFlippedY = not self.__mFlippedY
        
    def rotate(self, degrees):
        self.__mRotation = degrees
        
    def flippedX(self):
        return self.__mFlippedX
    
    def flippedY(self):
        return self.__mFlippedY
    
    def getRotation(self):
        return self.__mRotation
    
    def getWidth(self):
        return self.image.get_width()
    
    def getHeight(self):
        return self.image.get_height()
    
    
    
    