#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Box2D
from Box2D import *
from Model.Direction import *

class Player(object):
    
    mWorld = None;
    mBody = None;
    SPEED = 4
    mVelocity = b2Vec2_zero
    mGravityDirection = GravityDirection.DOWN
    mGravity = b2Vec2(0, -10)
    mDirection = b2Vec2(0,0)
    
    def __init__(self, position, world):
        self.mPosition = position
        self.mWorld = world
        
        #create player physicsbody
        self.mBody = world.CreateDynamicBody(position = self.mPosition)
        self.mBody.CreatePolygonFixture(box=(0.4,0.4), density=1, friction=0)
        
        #Fix for dynamic body getting stuck in static bodies sometimes
        self.mBody.CreateCircleFixture(radius=0.05, density=30, friction=0, pos=(0.4,0.4))
        self.mBody.CreateCircleFixture(radius=0.05, density=30, friction=0, pos=(-0.4,-0.4)) 
        self.mBody.CreateCircleFixture(radius=0.05, density=30, friction=0, pos=(-0.4,0.4)) 
        self.mBody.CreateCircleFixture(radius=0.05, density=30, friction=0, pos=(0.4,-0.4)) 
        self.mBody.fixedRotation = True
        self.mBody.userData = self
    
    def update(self, delta):
        self.mVelocity.Set(self.mDirection.x * self.SPEED, 0)
        self.mBody.linearVelocity = self.mGravity + self.mVelocity
        
    
    def __setVelocity(self, value):
        self.mVelocity = value

    def __getVelocity(self):
        return self.mVelocity
    
    def __getPosition(self):
        return self.mBody.position
    
    def goLeft(self):
        if self.mGravityDirection == GravityDirection.DOWN:
            self.mDirection.Set(FaceDirection.LEFT, 0)
        elif self.mGravityDirection == GravityDirection.UP:
            self.mDirection.Set(FaceDirection.LEFT, 0)
    
    def goRight(self):
        if self.mGravityDirection == GravityDirection.DOWN:
            self.mDirection.Set(FaceDirection.RIGHT, 0)
        elif self.mGravityDirection == GravityDirection.UP:
            self.mDirection.Set(FaceDirection.RIGHT, 0)
    
    def flipGravityX(self):
        self.mGravity.Set(self.mGravityDirection, 0)
    
    def flipGravityY(self):
        self.mGravity.Set(0, self.mGravityDirection)
    
    velocity = property(__getVelocity, __setVelocity)
    position = property(__getPosition, None)