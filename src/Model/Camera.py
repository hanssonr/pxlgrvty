#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Box2D import b2Vec2
import math

class Camera(object):
    
    CAMERA_WIDTH = 16.0
    CAMERA_HEIGHT = 10.0
    
    mScale = None
    mDisplacement = None
    mFrustumBias = 1.0
    
    def __init__(self, width, height):
        self.mScale = b2Vec2(width / self.CAMERA_WIDTH, height / self.CAMERA_HEIGHT)
        self.mDisplacement = b2Vec2(0, 0)
    
    def update(self, delta, pos, levelwidth, levelheight):
        self.displacement.x = pos.x - self.CAMERA_WIDTH / 2    
        self.displacement.y = pos.y - self.CAMERA_HEIGHT / 2
        
        #check X
        if self.CAMERA_WIDTH + self.displacement.x > levelwidth:
            self.displacement.x = levelwidth - self.CAMERA_WIDTH
        elif self.displacement.x < 0:
            self.displacement.x = 0
            
        #check Y
        if self.CAMERA_HEIGHT + self.displacement.y > levelheight:
            self.displacement.y = levelheight - self.CAMERA_HEIGHT
        elif self.displacement.y < 0:
            self.displacement.y = 0
          
    def __getScale(self):
        return self.mScale
    
    def __setScale(self, value):
        self.mScale = value
    
    def __getDisplacement(self):
        return self.mDisplacement
    
    def __setDisplacement(self, value):
        self.mDisplacement.Set(value.x, value.y)
        
    def getViewCoords(self, modelCoords):
        viewCoords = modelCoords.copy()
        viewCoords.x -= self.displacement.x
        viewCoords.y -= self.displacement.y
        viewCoords = b2Vec2(viewCoords.x * self.scale.x, viewCoords.y * self.scale.y)
        return viewCoords
    
    def getModelCoords(self, viewCoords):
        modelCoords = b2Vec2(viewCoords.x / self.scale.x, viewCoords.y / self.scale.y)
        modelCoords.x += self.displacement.x
        return modelCoords
    
    def getReversedYAxis(self, oldY):
        return (self.CAMERA_HEIGHT - oldY)
    
    def getScaledSize(self, x, y):
        return b2Vec2(x * self.scale.x, y * self.scale.y)
    
    def isInFrustum(self, x, y):
        return True if (x >= self.displacement.x - self.mFrustumBias and 
                x <= self.displacement.x + self.mFrustumBias + self.CAMERA_WIDTH and
                y >= self.displacement.y - self.mFrustumBias and
                y <= self.displacement.y + self.mFrustumBias + self.CAMERA_WIDTH) else False
    
     
    #properties  
    displacement = property(__getDisplacement, __setDisplacement, doc='Sets the displacement of the camera')
    scale = property(__getScale, __setScale)