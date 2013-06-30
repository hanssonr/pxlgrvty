"""
Singleton
http://blog.amir.rachum.com/post/21850841339/implementing-the-singleton-pattern-in-python
"""

import pygame, libs.pygl2d as gl

class Resources(object):

    INSTANCE = None
    
    mMud = None
    mPlayer = None
    mFont = None
    mLoaded = False
    
    def __init__(self):
        if self.INSTANCE is not None:
            raise ValueError("already instantiated")
    
    def loadGameResources(self):
        self.mMud = pygame.image.load("assets/gfx/mud.png").convert()
        self.mPlayer = pygame.image.load("assets/gfx/player.png").convert()
        self.mFont = pygame.font.SysFont('mono', 36)
        self.mFpsFont = pygame.font.Font("assets/fonts/visitor.ttf", 30)
        self.mLoaded = True
    
    @classmethod
    def getInstance(cls):
        if cls.INSTANCE is None:
            cls.INSTANCE = Resources()
        return cls.INSTANCE