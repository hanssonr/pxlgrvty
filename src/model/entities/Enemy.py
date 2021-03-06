"""
Baseclass of a Enemy, inherits Entity

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

from model.entities.Entity import Entity
from Box2D import b2PolygonShape, b2FixtureDef, b2CircleShape, b2EdgeShape, b2Vec2

class Enemy(Entity):

    def __init__(self, physworld, pos, size, shape, userdata):
        self.mWorld = physworld
        body = self.__createCollisionBody(pos, size, shape, userdata)
        super(Enemy, self).__init__(pos, size, body)

    def __createCollisionBody(self, pos, size, shape, ud = None):
        #collisionbody
        body = self.mWorld.CreateDynamicBody(position = pos)

        if shape == EnemyShape.CIRCLE:
            shape = b2CircleShape(radius=size.x/2)
        elif shape == EnemyShape.POLYGON:
            shape = b2PolygonShape()
            shape.SetAsBox(size.x/2, size.y/2)
        elif shape == EnemyShape.LINE:
            shape = b2EdgeShape()
            shape.vertices = b2Vec2(-size.x / 2.0, -size.y / 2.0), b2Vec2(size.x / 2.0, size.y / 2.0)

        fd = b2FixtureDef()
        fd.shape = shape
        fd.isSensor = True
        body.CreateFixture(fd)
        body.isbullet = False
        body.fixedRotation = True
        body.userData = self if ud == None else ud

        return body


class EnemyShape(object):
    POLYGON = 0
    CIRCLE = 1
    LINE = 2
