"""
Singleton
http://blog.amir.rachum.com/post/21850841339/implementing-the-singleton-pattern-in-python
"""

import pygame, libs.Options

class Resources(object):

    INSTANCE = None
    
    mPlayer = None
    mFont = None
    mBox = None
    mSpikeBox = None
    mSpike = None
    mLoaded = False
    mNugget = None
    mSwirlSheet = None
    mLevelButton = None
    mMenuButton = None
    mCheckButton = None
    mArrow = None
    mLock = None
    mMedallions = None
    
    def __init__(self):
        if self.INSTANCE is not None:
            raise ValueError("already instantiated")
    
    def loadGameResources(self):
        self.mBox = pygame.image.load("assets/gfx/box.png").convert()
        self.mPxl = pygame.image.load("assets/gfx/player.png").convert_alpha()
        self.mSpikeBox = pygame.image.load("assets/gfx/spikebox.png").convert_alpha()
        self.mSpike = pygame.image.load("assets/gfx/spike.png").convert_alpha()
        self.mNugget = pygame.image.load("assets/gfx/nugget.png").convert_alpha()
        self.mSwirlSheet = pygame.image.load("assets/gfx/swirl.png").convert_alpha()
        self.mLevelButton = pygame.image.load("assets/gfx/levelbutton.png").convert_alpha()
        self.mMenuButton = pygame.image.load("assets/gfx/menubutton.png").convert_alpha()
        self.mCheckButton = pygame.image.load("assets/gfx/checkbutton.png").convert_alpha()
        self.mArrow = pygame.image.load("assets/gfx/arrow.png").convert_alpha()
        self.mLock = pygame.image.load("assets/gfx/lock.png").convert_alpha()
        self.mMedallions = pygame.image.load("assets/gfx/medallions.png").convert_alpha()
        self.mFont = pygame.font.SysFont('mono', 36)
        self.mFpsFont = pygame.font.Font("assets/fonts/visitor.ttf", 30)
        
        self.mLoaded = True
    
    def getScaledFont(self, size):
        return pygame.font.Font("assets/fonts/visitor.ttf", int(size))
    
    @classmethod
    def getInstance(cls):
        if cls.INSTANCE is None:
            cls.INSTANCE = Resources()
        return cls.INSTANCE