#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Box2D import b2Vec2
import math

class Camera(object):
    
    CAMERA_WIDTH = 32.0
    CAMERA_HEIGHT = 20.0
    PPM = None
    
    mScale = None
    mDisplacement = None
    
    def __init__(self, width, height):
        self.PPM = width / self.CAMERA_WIDTH
        self.mScale = b2Vec2(width / self.CAMERA_WIDTH, height / self.CAMERA_HEIGHT)
        self.mDisplacement = b2Vec2(0, 0)
    
    def update(self, delta, pos, levelwidth, levelheight):
        if pos.x > self.CAMERA_WIDTH / 2:
            self.mDisplacement.x = pos.x - self.CAMERA_WIDTH / 2
            
            if self.CAMERA_WIDTH + self.mDisplacement.x > levelwidth:
                self.mDisplacement.x = levelwidth - self.CAMERA_WIDTH

        if pos.y > self.CAMERA_HEIGHT / 2:
            self.mDisplacement.y = pos.y - self.CAMERA_HEIGHT / 2
            
            if self.mDisplacement.y + self.CAMERA_HEIGHT > levelheight:
                self.mDisplacement.y = levelheight - self.CAMERA_HEIGHT
          
    def __getScale(self):
        return self.mScale
    
    def __setScale(self, value):
        self.mScale = value
    
    def __getDisplacement(self):
        return self.mDisplacement
    
    def __setDisplacement(self, value):
        self.mDisplacement.Set(value.x, value.y)
        
    def getViewCoords(self, modelCoords):
        modelCoords.x -= self.displacement.x
        modelCoords.y -= self.displacement.y
        modelCoords = b2Vec2(modelCoords.x * self.scale.x, modelCoords.y * self.scale.y)
        return modelCoords
    
    def getModelCoords(self, viewCoords):
        modelCoords = viewCoords / self.scale.x
        modelCoords.x += self.displacement.x
        modelCoords.y = self.getReversedYAxis(modelCoords.y)
        return modelCoords
    
    def getReversedYAxis(self, oldY):
        return (self.CAMERA_HEIGHT - oldY)
    
    def getScaledSize(self, x, y):
        return b2Vec2(x * self.mScale.x, y * self.mScale.y)
    
     
    #properties  
    displacement = property(__getDisplacement, __setDisplacement, doc='Sets the displacement of the camera')
    scale = property(__getScale, __setScale)