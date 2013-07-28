import Entity
from Box2D import b2PolygonShape, b2FixtureDef, b2CircleShape

class Enemy(Entity.Entity):
    
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
        
        fd = b2FixtureDef()
        fd.shape = shape
        fd.isSensor = True
        body.CreateFixture(fd)
        body.isbullet = True
        body.fixedRotation = True
        body.userData = self if ud == None else ud
        
        return body


class EnemyShape(object):
    POLYGON = 0
    CIRCLE = 1