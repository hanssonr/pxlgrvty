import SpikeBox, Entity
from Box2D import b2PolygonShape, b2FixtureDef


class Enemy(Entity.Entity):
    
    def __init__(self, physworld, pos, size, userdata):
        self.mWorld = physworld
        body = self.__createCollisionBody(pos, size, userdata)
        super(Enemy, self).__init__(pos, size, body)
    
    def __createCollisionBody(self, pos, size, ud = None):
        #collisionbody       
        body = self.mWorld.CreateDynamicBody(position = pos)
        shape = b2PolygonShape()
        shape.SetAsBox(size.x/2, size.y/2)
        fd = b2FixtureDef()
        fd.shape = shape
        fd.isSensor = False
        body.CreateFixture(fd)
        body.isbullet = True
        body.fixedRotation = True
        body.userData = self if ud == None else ud
        """
        if isinstance(ud, SpikeBox.SpikeBox):
            #create collisionsensor
            shape.SetAsBox(size.x/1.5, size.y/1.5, (0, 0), 0)
            fd.shape = shape
            fd.isSensor = True
            fd.userData = ud
            body.CreateFixture(fd)"""
        
        return body