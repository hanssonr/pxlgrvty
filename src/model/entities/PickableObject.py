"""
Baseclass for pickupable objects

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

from model.entities.Entity import Entity
from Box2D import *
from libs.SoundManager import SoundManager, SoundID

class PickableObject(Entity):

    def __init__(self, pos, physworld, size, userData):
        self.mWorld = physworld
        body = self.__createCollisionBody(pos, size, userData)
        super(PickableObject, self).__init__(pos, size, body)

    def __createCollisionBody(self, pos, size, ud):
        #collisionbody
        body = self.mWorld.CreateDynamicBody(position = pos)
        shape = b2PolygonShape()
        shape.SetAsBox(size.x/2, size.y/2)
        fd = b2FixtureDef()
        fd.shape = shape
        fd.isSensor = True
        body.CreateFixture(fd)
        body.userData = ud
        return body

    def update(self, delta):
        if not self.alive:
            SoundManager.getInstance().playSound(SoundID.PICKUP)
            self.mWorld.DestroyBody(self.mBody)
            
