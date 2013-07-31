from PickableObject import PickableObject
from Box2D import b2Vec2

class Crystal(PickableObject):
    
    __SIZE = b2Vec2(0.4, 0.4)
    
    def __init__(self, position, physworld):
        self.mPosition = b2Vec2(position[0] + 0.5, position[1] + 0.5) 
        super(Crystal, self).__init__(self.mPosition, physworld, self.__SIZE, self)