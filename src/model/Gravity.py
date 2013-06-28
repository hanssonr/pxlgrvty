import Box2D
from Box2D import b2Vec2
from Direction import GravityDirection

class Gravity(object):
    
    FORCE = 8
    __mGravity = b2Vec2(0, FORCE)
    
    
    def set(self, gravitydir):
        if gravitydir == GravityDirection.DOWN:
            self.__mGravity.Set(0, self.FORCE)
        elif gravitydir == GravityDirection.UP:
            self.__mGravity.Set(0, -self.FORCE)
        elif gravitydir == GravityDirection.LEFT:
            self.__mGravity.Set(-self.FORCE, 0)
        elif gravitydir == GravityDirection.RIGHT:
            self.__mGravity.Set(self.FORCE, 0)
    
    def get(self):
        return self.__mGravity
