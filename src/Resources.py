"""
Singleton
http://blog.amir.rachum.com/post/21850841339/implementing-the-singleton-pattern-in-python
"""

import pygame

class Resources(object):

    INSTANCE = None
    
    mMud = None
    mRock = None
    mPlayer = None
    mFont = None
    mBox = None
    mSpikeBox = None
    mLoaded = False
    mNugget = None
    
    def __init__(self):
        if self.INSTANCE is not None:
            raise ValueError("already instantiated")
    
    def loadGameResources(self):
        self.mBox = pygame.image.load("assets/gfx/box.png").convert()
        self.mPlayer = pygame.image.load("assets/gfx/player.png").convert()
        self.mCowboy = pygame.image.load("assets/gfx/playerAnimation.png").convert_alpha()
        self.mPxl = pygame.image.load("assets/gfx/testsprite.png").convert_alpha()
        self.mSpikeBox = pygame.image.load("assets/gfx/spikebox.png").convert_alpha()
        self.mNugget = pygame.image.load("assets/gfx/nugget.png").convert_alpha()
        self.mFont = pygame.font.SysFont('mono', 36)
        self.mFpsFont = pygame.font.Font("assets/fonts/visitor.ttf", 30)
        
        self.mLoaded = True
    
    @classmethod
    def getInstance(cls):
        if cls.INSTANCE is None:
            cls.INSTANCE = Resources()
        return cls.INSTANCE