"""
Class that makes an Sprite able to animate
"""

from pygame import Rect
from libs.Sprite import Sprite
from Box2D import b2Vec2

class Animation(Sprite):
    
    __mElapsedTime = None
    __mLooping = None
    __mRunning = None
    __mIsDone = None
    
    __mCurrentFrame = None
    __mCurrentRow = None
    __mDrawRect = None  
    
    def __init__(self, sprite, framesX, framesY, animationtime, size, looping = True, running = True):
        super(Animation, self).__init__(sprite)
        
        self.__mElapsedTime = 0.0
        self.__mLooping = looping
        self.__mRunning = running
        self.__mIsDone = False
        self.__mCurrentFrame = 0
        self.__mCurrentRow = 0
        self.__mDrawRect = None
        
        Sprite.setSize(self, size)
        self.__mFramesX = framesX
        self.__mFramesY = framesY
        self.__mFrameHeight = Sprite.getHeight(self) / framesY
        self.__mFrameWidth = Sprite.getWidth(self) / framesX
        self.__mMaxTime = animationtime / self.__mFramesX
        self.__mDrawRect = Rect(self.__mCurrentFrame * self.__mFrameWidth, self.__mCurrentRow * self.__mFrameHeight, self.__mFrameWidth, self.__mFrameHeight)
        
    
    def draw(self, delta, position):
        self.__mElapsedTime += delta
        
        if self.__mRunning:
            if self.__mElapsedTime > self.__mMaxTime:
                
                self.__mCurrentFrame += 1
                
                if self.__mLooping:
                    if self.__mCurrentFrame >= self.__mFramesX:
                        self.__mCurrentFrame = 0
                else:
                    if self.__mCurrentFrame >= self.__mFramesX:
                        self.__mIsDone = True
                        self.__mCurrentFrame = 0
                
                self.__mElapsedTime = 0.0
        
        
        Sprite.draw(self, position, self.__mDrawRect.move(self.__mCurrentFrame * self.__mFrameWidth, self.__mCurrentRow * self.__mFrameHeight))
    
    def freeze(self, frameX, frameY = 0):
        self.__mRunning = False
        self.__mCurrentFrame = frameX
        self.__mCurrentRow = frameY
    
    def continueAnimation(self):
        self.__mRunning = True
    
    def setLooping(self, looping):
        self.__mLooping = looping
        
    def gotoRow(self, row):
        if row <= self.__mFramesY:
            self.__mCurrentRow = row
    
    def isAnimationDone(self):
        return self.__mIsDone
    
    def reset(self):
        self.__mIsDone = False
        self.__mCurrentFrame = 0
        self.__mCurrentRow = 0
    
        
