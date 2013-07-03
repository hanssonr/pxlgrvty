from Entity import Entity
from Box2D import *

class PickableObject(Entity):
    
    __isAlive = True
    
    def __init__(self, pos, physworld, size, userData):
        self.mWorld = physworld
        body = self.__createCollisionBody(pos, size, userData)
        super(PickableObject, self).__init__(pos, size, body)
    
    def __createCollisionBody(self, pos, size, ud):
        #collisionbody       
        body = self.mWorld.CreateStaticBody(position = pos)
        shape = b2PolygonShape()
        shape.SetAsBox(size.x/2, size.y/2)
        fd = b2FixtureDef()
        fd.shape = shape
        fd.isSensor = True
        fd.userData = ud
        body.CreateFixture(fd)
        return body 
    
    def __isAlive(self):
        return self.__isAlive
    
    def __setIsAlive(self, isAlive):
        self.__isAlive = isAlive
    
    alive = property(__isAlive, __setIsAlive)
        