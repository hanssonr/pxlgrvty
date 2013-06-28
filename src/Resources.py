"""
Singleton
http://blog.amir.rachum.com/post/21850841339/implementing-the-singleton-pattern-in-python
"""

import pygame

class Resources(object):

    INSTANCE = None
    
    mMud = None
    mFont = None
    
    def __init__(self):
        if self.INSTANCE is not None:
            raise ValueError("already instantiated")
    
    def loadGameResources(self):
        self.mMud = pygame.image.load("assets/gfx/mud.png").convert()
        self.mFont = pygame.font.SysFont('mono', 36)
    
    @classmethod
    def getInstance(cls):
        if cls.INSTANCE is None:
            cls.INSTANCE = Resources()
        return cls.INSTANCE