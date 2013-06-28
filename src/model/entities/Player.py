#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Box2D
from Box2D import *
from model.Direction import *
from model.entities.MovableEntity import *
from model.Gravity import *

class Player(MovableEntity):
    
    mWorld = None;
    mGravity = None
    
    def __init__(self, position, world, gravity):  
        self.mWorld = world
        self.mGravity = gravity
        
        #create player physicsbody
        body = world.CreateDynamicBody(position = position)
        body.CreatePolygonFixture(box=(0.4,0.4), density=1, friction=0)
        
        #Fix for dynamic body getting stuck in static bodies sometimes
        body.CreateCircleFixture(radius=0.05, density=30, friction=0, pos=(0.4,0.4))
        body.CreateCircleFixture(radius=0.05, density=30, friction=0, pos=(-0.4,-0.4)) 
        body.CreateCircleFixture(radius=0.05, density=30, friction=0, pos=(-0.4,0.4)) 
        body.CreateCircleFixture(radius=0.05, density=30, friction=0, pos=(0.4,-0.4)) 
        body.fixedRotation = True
        body.userData = self
        
        super(Player, self).__init__(position, body, b2Vec2(0,0), 4, b2Vec2(0,0))
     
    def update(self, delta):
        self.mVelocity.Set(self.mDirection.x * self.mSpeed, self.mDirection.y * self.mSpeed)
        self.mBody.linearVelocity = self.mGravity.get() + self.mVelocity
        


