#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Box2D
from Box2D import *

class Player(object):
    
    mPosition = None;
    mWorld = None;
    mBody = None;
    SPEED = 2.5
    mVelocity = b2Vec2_zero
    
    def __init__(self, position, world):
        self.mPosition = position
        self.mWorld = world
        
        #create player physicsbody
        self.mBody = world.CreateDynamicBody(position = self.mPosition)
        self.mBody.CreatePolygonFixture(box=(0.5,1), density=50, friction=0)
        self.mBody.fixedRotation = True
        self.mBody.userData = self
    
    def update(self, delta):
        self.mBody.linearVelocity = self.mVelocity
    
    def __setVelocity(self, value):
        self.mVelocity = value

    def __getVelocity(self):
        return self.mVelocity
    
    velocity = property(__getVelocity, __setVelocity)