#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Basklass för alla rörliga objekt
"""
import Box2D
from Box2D import b2Vec2

class Entity(object):
    
    mPosition = None
    mBody = None
    mInGravityZone = 0
    mOldGravity = None
    mSize = b2Vec2(0,0)
    
    def __init__(self, pos, size, physbody):
        self.mPosition = pos
        self.mSize = size
        self.mBody = physbody
    
    def __getPosition(self):
        return self.mBody.position
    
    def __setPosition(self, pos, angle):
        self.mBody.transform(pos, angle)
    
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
    
    position = property(__getPosition, __setPosition)
    size = property(__getSize, None)