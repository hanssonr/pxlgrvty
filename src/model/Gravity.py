import Box2D
from Box2D import b2Vec2
from Direction import GravityDirection

class Gravity(object):
    
    FORCE = None
    __mGravity = None
    __mGravityDir = None
    
    def __init__(self):
        self.FORCE = 6
        self.__mGravity = b2Vec2(0, self.FORCE)
        self.__mGravityDir = GravityDirection.DOWN
    
    def set(self, gravitydir):
        self.__mGravityDir = gravitydir
        
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
    
    def getGravityDirection(self):
        return self.__mGravityDir
