#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Box2D, math
from Box2D import *
from model.Direction import *
from model.entities.MovableEntity import *
from model.Gravity import *

class Player(MovableEntity):
    
    PLAYER_WIDTH = 0.9
    PLAYER_HEIGHT = 1.0
    
    mWorld = None;
    mGravity = None
    mSensor = None
    mOnGround = 0
    mInGravityZone = 0
    mOldGravity = None
    mGravityToUse = b2Vec2_zero
    mDelayedFlip = None
    
    mFacing = Facing.RIGHT
    mUpsideDown = False
    
    def __init__(self, position, world, gravity):  
        self.mWorld = world
        self.mGravity = gravity
        
        #create player physicsbody
        body = world.CreateDynamicBody(position = position)
        shape = b2PolygonShape()
        fd = b2FixtureDef()
        fd.shape = shape
        fd.isSensor = True
        
        #footsensor
        shape.SetAsBox(0.35, 0.1, (0, 0.4), 0)
        fd.userData = Sensor.FOOTSENSOR
        body.CreateFixture(fd)
        
        #gravitysensor
        shape.SetAsBox(0.1,0.1)
        fd.userData = Sensor.GRAVITYZONESENSOR
        body.CreateFixture(fd)
        
        #collisionbody
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
        #do we have a delayed flip, do it
        if self.mDelayedFlip != None:
            self.flip(self.mDelayedFlip)
            self.mDelayedFlip = None
        
        if self.mOldGravity != None:
            self.mGravityToUse.Set(self.mOldGravity.x, self.mOldGravity.y)
        else:
            self.mGravityToUse.Set(self.mGravity.get().x, self.mGravity.get().y)
            
        self.mVelocity.Set(self.mDirection.x * self.mSpeed, self.mDirection.y * self.mSpeed)    
        self.mBody.linearVelocity = self.mGravityToUse + self.mVelocity
        
        if self.mVelocity.x > 0:
            self.mFacing = Facing.RIGHT
        elif self.mVelocity.x < 0:
            self.mFacing = Facing.LEFT
        elif self.mVelocity.y > 0:
            self.mFacing = Facing.UP
        elif self.mVelocity.y < 0:
            self.mFacing = Facing.DOWN
    
    def flip(self, direction):
        if direction == GravityDirection.UP:
            self.mBody.transform = (self.mBody.position, math.radians(180))
            self.mUpsideDown = True
        elif direction == GravityDirection.DOWN:
            self.mBody.transform = (self.mBody.position, math.radians(0))
            self.mUpsideDown = False
        elif direction == GravityDirection.LEFT:
            self.mBody.transform = (self.mBody.position, math.radians(90))
        elif direction == GravityDirection.RIGHT:
            self.mBody.transform = (self.mBody.position, math.radians(270))
    
    def enterGravityZone(self):
        self.mInGravityZone += 1
         
        if self.mOldGravity == None and self.mInGravityZone == 1:
            self.mOldGravity = b2Vec2(self.mGravity.get().x, self.mGravity.get().y)
    
    def exitGravityZone(self):
        self.mInGravityZone -= 1
        
        if self.mInGravityZone == 0:
            self.mOldGravity = None
            self.mDelayedFlip = self.mGravity.getGravityDirection()
    
    def isOnGround(self):
        return self.mOnGround > 0
    
    def isInGravityZone(self):
        return self.mInGravityZone > 0
    
    def getRenderPosition(self):
        return b2Vec2(self.position.x - self.PLAYER_WIDTH / 2, self.position.y - self.PLAYER_HEIGHT / 2)


class Sensor():
    FOOTSENSOR = 1
    GRAVITYZONESENSOR = 2


