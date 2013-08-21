#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Baseclass for moveable entities

Author: Rickard Hansson, rkh.hansson@gmail.com
"""


from model.entities.Entity import *
from model.Direction import MoveDirection, Direction
    
class MovableEntity(Entity):
    
    mVelocity = b2Vec2(0,0)
    mSpeed = None
    mDirection = None
    
    def __init__(self, pos, size, physbody, velocity, speed, movedir):
        self.mVelocity = velocity
        self.mSpeed = speed
        self.mDirection = movedir
        
        super(MovableEntity, self).__init__(pos, size, physbody)
    
    def __setVelocity(self, value):
        self.mVelocity = value

    def __getVelocity(self):
        return self.mBody.linearVelocity
    
    def move(self, movedir):
        if movedir == MoveDirection.UP:
            self.mDirection.Set(0, Direction.UP)
        if movedir == MoveDirection.DOWN:
            self.mDirection.Set(0, Direction.DOWN)
        if movedir == MoveDirection.LEFT:
            self.mDirection.Set(Direction.LEFT, 0)
        if movedir == MoveDirection.RIGHT:
            self.mDirection.Set(Direction.RIGHT, 0)
    
    def flip(self, direction):
        self.mOldGravity = None
    
    velocity = property(__getVelocity, __setVelocity)