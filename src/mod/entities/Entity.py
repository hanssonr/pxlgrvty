#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Baseclass for all objects

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

from Box2D import b2Vec2
from libs.Id import Id

class Entity(object):
    
    mId = None
    mPosition = None
    mBody = None
    mInGravityZone = 0
    mOldGravity = None
    mSize = b2Vec2(0,0)
    __mAlive = None
    
    def __init__(self, pos, size, physbody):
        self.__mAlive = True
        self.mId = Id.getInstance().getId()
        self.mPosition = pos
        self.mSize = size
        self.mBody = physbody
    
    def __getPosition(self):
        return self.mBody.position
    
    def __setPosition(self, pos, angle):
        self.mBody.transform = (pos, angle)
    
    def enterGravityZone(self):
        self.mInGravityZone += 1
         
        if self.mOldGravity == None and self.mInGravityZone == 1:
            self.mOldGravity = b2Vec2(self.mGravity.get().x, self.mGravity.get().y)
    
    def exitGravityZone(self):
        self.mInGravityZone -= 1
    
    def isInGravityZone(self):
        return self.mInGravityZone > 0
    
    def stopMovement(self):
        self.mBody.linearVelocity = b2Vec2(0,0)

    def __getSize(self):
        return self.mSize
    
    def __setSize(self, size):
        self.mSize = size
    
    def getBody(self):
        return self.mBody
    
    def __isAlive(self):
        return self.__mAlive
    
    def __setIsAlive(self, isAlive):
        self.__mAlive = isAlive
        
    def __getId(self):
        return self.mId
    
    def isActive(self):
        return self.mBody.active

    id = property(__getId, None)   
    alive = property(__isAlive, __setIsAlive)
    position = property(__getPosition, lambda self, value: self.__setPosition(*value))
    size = property(__getSize, __setSize)