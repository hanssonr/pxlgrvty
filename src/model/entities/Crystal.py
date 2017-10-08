"""
A pickupable item in form of a crystal, opens portals

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

from model.entities.PickableObject import PickableObject
from Box2D import b2Vec2
import random

class Crystal(PickableObject):

    __SIZE = b2Vec2(0.4, 0.4)
    __mMoveTimer = None
    __mVelocity = None
    __mDirection = None
    __mDelay = None

    def __init__(self, position, physworld):
        random.seed(position[0] + position[1])
        self.__mDelay = random.uniform(0.5, 1.5)
        self.__mDirection = b2Vec2(0, 1 if random.randint(0,1) == 0 else -1)
        self.__mMoveTimer = 1.0
        self.__mVelocity = 0.1
        self.mPosition = b2Vec2(position[0] + 0.5, position[1] + 0.5)
        super(Crystal, self).__init__(self.mPosition, physworld, self.__SIZE, self)

    def update(self, delta):
        if self.__mDelay > 0:
            self.__mDelay -= delta

        if self.__mDelay <= 0:
            self.__mMoveTimer -= delta
            if self.__mMoveTimer < 0:
                self.__mMoveTimer = 1.0
                self.__mDirection *= -1

            self.mBody.linearVelocity = self.__mDirection * self.__mVelocity

        super(Crystal, self).update(delta)
