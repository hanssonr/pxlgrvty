from Box2D import b2Vec2
from Enemy import Enemy, EnemyShape
from model.Direction import MoveDirection
import math


class Saw(Enemy):
    
    __mCurrent = None
    __mTarget = None
    mSpeed = None
    __mLength = None

    
    def __init__(self, physworld, pos, movepattern, radius, speed):
        self.__mTarget = b2Vec2(0,0)
        self.__mCurrent = len(movepattern)-1
        self.mPattern = movepattern
        self.mSpeed = speed
        super(Saw, self).__init__(physworld, pos, b2Vec2(radius, radius), EnemyShape.CIRCLE, self)
        self.calculateTarget()
    
    
    def update(self, delta):

        if self.__mLength == 0:
            self.mBody.transform = self.__mTarget, 0 
            self.calculateTarget()
        else:
            direction = self.__mTarget.copy() - self.mBody.position.copy()
            direction.Normalize()
            velocity = direction * self.mSpeed
            if self.__mLength - velocity.copy().length * delta > 0:
                self.__mLength -= velocity.copy().length * delta
            else:
                velocity = direction * (self.__mLength / delta)
                self.__mLength = 0
                
            self.mBody.linearVelocity = velocity
            
        
    def calculateTarget(self):
        self.__mCurrent = 0 if self.__mCurrent + 1 > len(self.mPattern)-1 else self.__mCurrent + 1
        direction = int(self.mPattern[self.__mCurrent][0])
        self.__mLength = int(self.mPattern[self.__mCurrent][1])
        
        if direction == MoveDirection.UP:
            self.__mTarget.Set(self.mBody.position.x, self.mBody.position.y - self.__mLength)
        elif direction == MoveDirection.RIGHT:
            self.__mTarget.Set(self.mBody.position.x + self.__mLength, self.mBody.position.y)
        elif direction == MoveDirection.DOWN:
            self.__mTarget.Set(self.mBody.position.x, self.mBody.position.y + self.__mLength)
        else:
            self.__mTarget.Set(self.mBody.position.x - self.__mLength, self.mBody.position.y)
            