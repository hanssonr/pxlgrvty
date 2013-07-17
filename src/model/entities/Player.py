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
    mJumping = False
    mGravityToUse = b2Vec2_zero
    mPlayerState = None
    
    mJumpTimer = 0
    
    mFacing = Facing.RIGHT
    mBodyDirection = GravityDirection.DOWN
    
    def __init__(self, position, physworld, gravity):  
        self.mWorld = physworld
        self.mGravity = gravity
        self.mPlayerState = PlayerState.IDLE
        
        #create player physicsbody
        pos = b2Vec2(position[0] + self.PLAYER_WIDTH/3, position[1] + self.PLAYER_HEIGHT/2)
        body = self.mWorld.CreateDynamicBody(position = pos)
        shape = b2PolygonShape()
        fd = b2FixtureDef()
        fd.shape = shape
        fd.isSensor = True
        
        #footsensor
        shape.SetAsBox(self.PLAYER_WIDTH/3.6, 0.1, (0, 0.4), 0)
        fd.userData = Sensor.PLAYER_FOOTSENSOR
        body.CreateFixture(fd)
        
        #gravitysensor
        shape.SetAsBox(0.1,0.1)
        fd.userData = Sensor.GRAVITYZONESENSOR
        body.CreateFixture(fd)
        
        #collisionbody
        body.CreatePolygonFixture(box=(self.PLAYER_WIDTH/3.5, self.PLAYER_HEIGHT/2), density=0, friction=0)
        body.bullet = True
        body.fixedRotation = True
        body.userData = self
              
        super(Player, self).__init__(pos, b2Vec2(self.PLAYER_WIDTH, self.PLAYER_HEIGHT), body, b2Vec2(0,0), 3.5, b2Vec2(0,0))
     
    def update(self, delta): 
        if self.mOldGravity != None:
            self.mGravityToUse = self.mOldGravity.copy()
        else:
            self.mGravityToUse = self.mGravity.get().copy()
        
        #setting velocity
        self.mVelocity = self.mDirection.copy() * self.mSpeed
        
        #jumping
        if self.mJumping:
            #changing velocity depending on bodyDirection due to gravity
            if self.mBodyDirection == GravityDirection.LEFT or self.mBodyDirection == GravityDirection.RIGHT:
                self.mVelocity.x = -self.mGravityToUse.x * 0.78
            else:
                self.mVelocity.y = -self.mGravityToUse.y * 0.78
            
            #zero out gravity
            self.mGravityToUse = b2Vec2(0,0)
            
            self.mJumpTimer += delta
            if self.mJumpTimer > 0.3:
                self.mJumpTimer = 0
                self.mJumping = False
  
        self.mBody.linearVelocity = self.mGravityToUse + self.mVelocity
        
        #Facing
        if self.mVelocity.x > 0:
            if self.mBodyDirection == GravityDirection.DOWN or self.mBodyDirection == GravityDirection.UP:
                self.mFacing = Facing.RIGHT
        elif self.mVelocity.x < 0:
            if self.mBodyDirection == GravityDirection.DOWN or self.mBodyDirection == GravityDirection.UP:
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
                   
                
        if self.mVelocity.x > 0 or self.mVelocity.x < 0 or self.mVelocity.y > 0 or self.mVelocity.y < 0:
            self.mPlayerState = PlayerState.MOVING
        else:
            self.mPlayerState = PlayerState.IDLE
        
        if self.mOnGround == False:
            self.mPlayerState = PlayerState.FALLING
    
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
    
    def jump(self):
        if self.mOnGround:
            print "jumping"
            self.mJumping = True

class PlayerState():
    IDLE = 0
    MOVING = 1
    FALLING = 2
