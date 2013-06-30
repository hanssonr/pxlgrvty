#!/usr/bin/env python
# -*- coding: utf-8 -*-

from model.entities.Entity import *
from model.Direction import MoveDirection, Direction
    
class MovableEntity(Entity):
    
    mVelocity = None
    mSpeed = None
    mDirection = None
    
    def __init__(self, pos, physbody, velocity, speed, movedir):
        self.mVelocity = velocity
        self.mSpeed = speed
        self.mDirection = movedir
        
        super(MovableEntity, self).__init__(pos, physbody)
    
    def __setVelocity(self, value):
        self.mVelocity = value

    def __getVelocity(self):
        return self.mVelocity
    
    def move(self, movedir):
        if movedir == MoveDirection.UP:
            self.mDirection.Set(0, Direction.UP)
        if movedir == MoveDirection.DOWN:
            self.mDirection.Set(0, Direction.DOWN)
        if movedir == MoveDirection.LEFT:
            self.mDirection.Set(Direction.LEFT, 0)
        if movedir == MoveDirection.RIGHT:
            self.mDirection.Set(Direction.RIGHT, 0)
    
    velocity = property(__getVelocity, __setVelocity)