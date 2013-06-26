#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Box2D
from Box2D import *
from Model.Direction import *

class Player(object):
    
    mWorld = None;
    mBody = None;
    SPEED = 5.5
    mVelocity = b2Vec2_zero
    mGravityDirection = GravityDirection.DOWN
    mGravity = b2Vec2(0, -9.2)
    mDirection = b2Vec2(0,0)
    
    def __init__(self, position, world):
        self.mPosition = position
        self.mWorld = world
        
        #create player physicsbody
        self.mBody = world.CreateDynamicBody(position = self.mPosition)
        self.mBody.CreatePolygonFixture(box=(0.4,0.4), density=50, friction=0)
        #self.mBody.CreateCircleFixture(radius=0.3, density=30, friction=0, pos=(0,-0.2)) 
        self.mBody.fixedRotation = True
        self.mBody.userData = self
    
    def update(self, delta):
        pass
        #print self.mGravity
        #self.mVelocity = self.mDirection * self.SPEED
        #self.mBody.linearVelocity = self.mVelocity
        
    
    def __setVelocity(self, value):
        self.mVelocity = value

    def __getVelocity(self):
        return self.mVelocity
    
    def __getPosition(self):
        return self.mBody.position
    
    def goLeft(self):
        if self.mGravityDirection == GravityDirection.DOWN:
            self.mDirection.Set(FaceDirection.LEFT, self.mGravity.y)
        elif self.mGravityDirection == GravityDirection.UP:
            pass
    
    def goRight(self):
        if self.mGravityDirection == GravityDirection.DOWN:
            self.mDirection.Set(FaceDirection.RIGHT, self.mGravity.y)
        elif self.mGravityDirection == GravityDirection.UP:
            pass
    
    velocity = property(__getVelocity, __setVelocity)
    position = property(__getPosition, None)