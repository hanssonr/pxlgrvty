#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Box2D
from Box2D import *
from Libs.Pgl import *

class Camera(object):
    
    CAMERA_WIDTH = 32.0
    CAMERA_HEIGHT = 20.0
    PPM = None
    
    mScale = None
    mDisplacement = None
    
    def __init__(self, width, height):
        self.PPM = width / self.CAMERA_WIDTH
        self.mScale = b2Vec2(width / self.CAMERA_WIDTH, height / self.CAMERA_HEIGHT)
        self.mDisplacement = b2Vec2(0.5, self.CAMERA_HEIGHT+0.5)
          
    def __getScale(self):
        return self.mScale
    
    def __setScale(self, value):
        print value
        self.mScale = value
    
    def __getDisplacement(self):
        return self.mDisplacement
    
    def __setDisplacement(self, value):
        self.mDisplacement = value
        
    def getViewCoordinats(self, modelCoords):
        modelCoords.x += self.displacement.x
        modelCoords.y += self.displacement.y
        modelCoords = b2Vec2(modelCoords.x * self.scale.x, modelCoords.y * self.scale.y)
        return modelCoords
    
    def getModelCoordinats(self, viewCoords):
        modelCoords = viewCoords / self.scale.x
        modelCoords.x += self.displacement.x
        modelCoords.y = self.getReversedYAxis(modelCoords.y) + self.displacement.y
        return modelCoords
    
    def getReversedYAxis(self, oldY):
        return (self.CAMERA_HEIGHT - oldY)
    
    
    
    #properties
    
    displacement = property(__getDisplacement, __setDisplacement, doc='Sets the displacement of the camera')
    scale = property(__getScale, __setScale)