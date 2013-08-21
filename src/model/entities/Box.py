"""
Boxclass, moveable enitity, *NOT USED*
"""

from model.Sensor import *
from Box2D import b2Vec2, b2Vec2_zero, b2PolygonShape, b2FixtureDef
from MovableEntity import MovableEntity

class Box(MovableEntity):
    
    BOX_WIDTH = 0.95
    BOX_HEIGHT = 0.98
    mOldPos = b2Vec2_zero
    
    def __init__(self, position, world, gravity):
        self.mWorld = world
        self.mGravity = gravity 
        pos = b2Vec2(position[0] + self.BOX_WIDTH/2, position[1] + self.BOX_HEIGHT/2)
        
        #create box physicsbody
        body = world.CreateDynamicBody(position = pos)
        shape = b2PolygonShape()
        fd = b2FixtureDef()
        fd.shape = shape
        fd.isSensor = True
        
        #gravitysensor
        shape.SetAsBox(0.1,0.1)
        fd.userData = Sensor.GRAVITYZONESENSOR
        body.CreateFixture(fd)
        
        #collisionbody
        body.CreatePolygonFixture(box=(self.BOX_WIDTH/2, self.BOX_HEIGHT/2), density=6, friction=0)
        
        body.fixedRotation = True
        body.bullet = True
        body.allowSleep = False
        body.mass = 2
        body.userData = self
        
        super(Box, self).__init__(pos, b2Vec2(self.BOX_WIDTH, self.BOX_HEIGHT), body, b2Vec2(0,0), 0, b2Vec2(0,0))
    
    def update(self, delta):
        if self.mOldGravity != None:
            self.mGravityToUse = self.mOldGravity.copy()
        else:
            self.mGravityToUse = self.mGravity.get().copy()
        
        self.mBody.linearVelocity = self.mGravityToUse
    
    def isMoving(self):
        return True if self.mOldPos.copy().Normalize() != self.mBody.position.copy().Normalize() else False
        
        