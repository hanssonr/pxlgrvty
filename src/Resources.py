"""
Resourcemanagement through singleton-pattern
Loads the resources before the game is operatable

http://blog.amir.rachum.com/post/21850841339/implementing-the-singleton-pattern-in-python

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

import pygame

class Resources(object):

    INSTANCE = None
    
    #gfx
    mPlayer = None
    mSpikeBox = None
    mSpike = None
    mCrystal = None
    mSwirlSheet = None
    mLevelButton = None
    mMenuButton = None
    mCheckButton = None
    mArrow = None
    mLock = None
    mMedallions = None
    mBlood = None
    mSaw = None
    mUI = None
    mLasermount = None
    
    #sound
    mFleshExplosion = None
    mJump = None
    
    def __init__(self):
        if self.INSTANCE is not None:
            raise ValueError("already instantiated")
    
    def loadGameResources(self):
        #gfx
        self.mPxl = pygame.image.load("assets/gfx/player.png").convert_alpha()
        self.mSpikeBox = pygame.image.load("assets/gfx/spikebox.png").convert_alpha()
        self.mSpike = pygame.image.load("assets/gfx/spike.png").convert_alpha()
        self.mSaw = pygame.image.load("assets/gfx/saw.png").convert_alpha()
        self.mLasermount = pygame.image.load("assets/gfx/lasermount.png").convert_alpha()
        self.mCrystal = pygame.image.load("assets/gfx/crystal.png").convert_alpha()
        self.mSwirlSheet = pygame.image.load("assets/gfx/swirl.png").convert_alpha()
        self.mLevelButton = pygame.image.load("assets/gfx/levelbutton.png").convert_alpha()
        self.mMenuButton = pygame.image.load("assets/gfx/menubutton.png").convert_alpha()
        self.mCheckButton = pygame.image.load("assets/gfx/checkbutton.png").convert_alpha()
        self.mArrow = pygame.image.load("assets/gfx/arrow.png").convert_alpha()
        self.mLock = pygame.image.load("assets/gfx/lock.png").convert_alpha()
        self.mMedallions = pygame.image.load("assets/gfx/medallions.png").convert_alpha()
        self.mUI = pygame.image.load("assets/gfx/ui.png").convert_alpha()
        self.mBlood = pygame.image.load("assets/gfx/blood.png").convert_alpha()
        
        #sound
        pygame.mixer.init()
        self.mFleshExplosion = pygame.mixer.Sound("assets/audio/sound/fleshexplosion.ogg")
        self.mJump = pygame.mixer.Sound("assets/audio/sound/jump.ogg")
        self.mPickup = pygame.mixer.Sound("assets/audio/sound/pickup.ogg")
    
    def getScaledFont(self, size):
        return pygame.font.Font("assets/fonts/visitor.ttf", int(size))
    
    @classmethod
    def getInstance(cls):
        if cls.INSTANCE is None:
            cls.INSTANCE = Resources()
        return cls.INSTANCE
    