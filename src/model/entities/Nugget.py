from PickableObject import PickableObject
from Box2D import b2Vec2

class Nugget(PickableObject):
    
    __NUGGETSIZE = 0.5
    
    def __init__(self, position, physworld):
        self.mPosition = b2Vec2(float(position[0]) + self.__NUGGETSIZE, float(position[1]) + self.__NUGGETSIZE) 
        super(Nugget, self).__init__(self.mPosition, physworld, b2Vec2(self.__NUGGETSIZE, self.__NUGGETSIZE), self)