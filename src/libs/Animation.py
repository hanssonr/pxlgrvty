"""
Class that makes an Sprite able to animate
"""

from pygame import Rect
from libs.Sprite import Sprite
from Box2D import b2Vec2

class Animation(Sprite):
    
    __mElapsedTime = 0.0
    __mLooping = True
    __mRunning = True
    
    __mCurrentFrame = 0
    __mCurrentRow = 0
    __mDrawRect = None  
    
    def __init__(self, sprite, framesX, framesY, animationtime, size):
        super(Animation, self).__init__(sprite)
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
    
        