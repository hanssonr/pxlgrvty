"""
Enemyclass for spikes

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

from Box2D import b2Vec2
from Enemy import Enemy, EnemyShape
from model.Direction import Facing

class Spike(Enemy):
    
    __SIZE = b2Vec2(0,0)
    mFacing = None
    
    def __init__(self, physworld, pos, facing):
        position = b2Vec2(pos[0], pos[1])
        self.mFacing = facing

        if facing == Facing.UP:
            self.__SIZE.Set(1, 0.5)
            position.Set(position.x + self.__SIZE.x / 2, position.y - self.__SIZE.y / 2.5 + 1.0)
        elif facing == Facing.DOWN:
            self.__SIZE.Set(1, 0.5)
            position.Set(position.x + self.__SIZE.x / 2, position.y + self.__SIZE.y / 2.5)
        elif facing == Facing.LEFT:
            self.__SIZE.Set(0.5, 1)
            position.Set(position.x - self.__SIZE.x / 2.5 + 1.0, position.y + self.__SIZE.y / 2)
        elif facing == Facing.RIGHT:
            self.__SIZE.Set(0.5, 1)
            position.Set(position.x + self.__SIZE.x / 2.5, position.y + self.__SIZE.y / 2.0)
        
        super(Spike, self).__init__(physworld, position, self.__SIZE, EnemyShape.POLYGON, self)
    
    def update(self, delta):
        pass