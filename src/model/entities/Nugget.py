from PickableObject import PickableObject
from Box2D import b2Vec2

class Nugget(PickableObject):
    
    __NUGGETSIZE = b2Vec2(0.25, 0.25)
    
    def __init__(self, position, physworld):
        self.mPosition = b2Vec2(position[0] + 0.5, position[1] + 0.5) 
        super(Nugget, self).__init__(self.mPosition, physworld, self.__NUGGETSIZE, self)