#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Box2D, math
from Box2D import *
from model.Direction import *
from model.entities.MovableEntity import *
from model.Gravity import *
from model.Sensor import *

class Player(MovableEntity):
    
    PLAYER_WIDTH = 0.75
    PLAYER_HEIGHT = 0.9
    
    mWorld = None;
    mGravity = None
    mSensor = None
    mOnGround = 0
    mGravityToUse = b2Vec2_zero
    mDelayedFlip = None
    
    mFacing = Facing.RIGHT
    mUpsideDown = False
    mLeftWallClimbing = False
    mBodyDirection = GravityDirection.DOWN
    
    def __init__(self, position, physworld, gravity):  
        self.mWorld = physworld
        self.mGravity = gravity
        
        #create player physicsbody
        pos = b2Vec2(position[0] + self.PLAYER_WIDTH/2, position[1] + self.PLAYER_HEIGHT/2)
        body = self.mWorld.CreateDynamicBody(position = pos)
        shape = b2PolygonShape()
        fd = b2FixtureDef()
        fd.shape = shape
        fd.isSensor = True
        
        #footsensor
        shape.SetAsBox(self.PLAYER_WIDTH/2.2, 0.1, (0, 0.4), 0)
        fd.userData = Sensor.PLAYER_FOOTSENSOR
        body.CreateFixture(fd)
        
        #gravitysensor
        shape.SetAsBox(0.1,0.1)
        fd.userData = Sensor.GRAVITYZONESENSOR
        body.CreateFixture(fd)
        
        #collisionbody
        body.CreatePolygonFixture(box=(self.PLAYER_WIDTH/2, self.PLAYER_HEIGHT/2), density=10, friction=0)
        body.bullet = True
        body.fixedRotation = True
        body.userData = self
              
        super(Player, self).__init__(pos, b2Vec2(self.PLAYER_WIDTH, self.PLAYER_HEIGHT), body, b2Vec2(0,0), 4, b2Vec2(0,0))
     
    def update(self, delta): 
        if self.mOldGravity != None:
            self.mGravityToUse = self.mOldGravity.copy()
        else:
            self.mGravityToUse = self.mGravity.get().copy()
               
        self.mVelocity.Set(self.mDirection.x * self.mSpeed, self.mDirection.y * self.mSpeed)    
        self.mBody.linearVelocity = self.mGravityToUse + self.mVelocity
        
        
        #spriteorientation
        if self.mVelocity.x > 0:
            self.mFacing = Facing.RIGHT
        elif self.mVelocity.x < 0:
            self.mFacing = Facing.LEFT
        elif self.mVelocity.y < 0:
            if self.mBodyDirection == GravityDirection.LEFT:
                self.mFacing = Facing.LEFT
            elif self.mBodyDirection == GravityDirection.RIGHT:
                self.mFacing = Facing.RIGHT
        elif self.mVelocity.y > 0:
            if self.mBodyDirection == GravityDirection.LEFT:
                self.mFacing = Facing.RIGHT
            elif self.mBodyDirection == GravityDirection.RIGHT:
                self.mFacing = Facing.LEFT
    
    def flip(self, direction):
        MovableEntity.flip(self, direction)
        
        self.mBodyDirection = direction
        
        if direction == GravityDirection.UP:
            self.mBody.transform = (self.mBody.position, math.radians(180))  
        elif direction == GravityDirection.DOWN:
            self.mBody.transform = (self.mBody.position, math.radians(0))
        elif direction == GravityDirection.LEFT:
            self.mBody.transform = (self.mBody.position, math.radians(90))
        elif direction == GravityDirection.RIGHT:
            self.mBody.transform = (self.mBody.position, math.radians(270))
    
 
    def isOnGround(self):
        return self.mOnGround > 0


