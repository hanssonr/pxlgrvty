"""
A particle of an effect

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

from Box2D import b2PolygonShape, b2FixtureDef
from model.Filter import *

class Particle(object):
    
    mVelocity = None
    mBody = None
    mSpeed = 8
    mIsAlive = None
    mLifetime = None
    
    
    def __init__(self, physworld, gravity, size, lifetime, pos):
        self.mWorld = physworld
        self.mGravity = gravity
        self.mSize = size
        self.mLifetime = lifetime
        self.mIsAlive = True
        
        #create body
        self.mBody = self.mWorld.CreateDynamicBody(position = pos)
        shape = b2PolygonShape()
        shape.SetAsBox(self.mSize.x/2.0,self.mSize.y/2.0)
        fd = b2FixtureDef()
        fd.shape = shape
        fd.categoryBits = Filter.CATEGORY_FX
        fd.maskBits = Filter.MASK_FX
        self.mBody.CreateFixture(fd)
        self.mBody.userData = self
        
    
    def update(self, delta):
        self.mVelocity.y += delta * 20
        self.mBody.linearVelocity = self.mGravity + self.mVelocity
        
        self.mLifetime -= delta
        
        if self.mLifetime <= 0:
            self.mIsAlive = False
            self.destroy()
    
    def destroy(self):
        self.mWorld.DestroyBody(self.mBody)
        
    def __getPosition(self):
        return self.mBody.position

    def __getIsAlive(self):
        return self.mIsAlive
    
    position = property(__getPosition, None)
    alive = property(__getIsAlive, None)
        