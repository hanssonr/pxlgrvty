"""
Enemyclass for a Saw

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

from Box2D import b2Vec2
from Enemy import Enemy, EnemyShape
from model.Direction import MoveDirection


class Saw(Enemy):
    
    __mCurrent = None
    __mTarget = None
    __mSpeed = None
    __mLength = None
    __mPattern = None

    
    def __init__(self, physworld, pos, movepattern, radius, speed):
        self.__mTarget = b2Vec2(0,0)
        self.__mCurrent = len(movepattern)-1
        self.__mPattern = movepattern
        self.__mSpeed = speed
        super(Saw, self).__init__(physworld, pos, b2Vec2(radius, radius), EnemyShape.CIRCLE, self)
        self.calculateTarget()
    
    
    def update(self, delta):
        #check length to next target
        if self.__mLength == 0:
            self.mBody.transform = self.__mTarget, 0 
            self.calculateTarget()
        else:
            #calculate direction
            direction = self.__mTarget.copy() - self.mBody.position.copy()
            direction.Normalize()
            velocity = direction * self.__mSpeed
            
            #if current speed is to high to reach next destination, calculate required speed
            if self.__mLength - velocity.copy().length * delta > 0:
                self.__mLength -= velocity.copy().length * delta
            else:
                velocity = direction * (self.__mLength / delta)
                self.__mLength = 0
                
            self.mBody.linearVelocity = velocity
            
    
    #Calculate next target
    def calculateTarget(self):
        self.__mCurrent = 0 if self.__mCurrent + 1 > len(self.__mPattern)-1 else self.__mCurrent + 1
        direction = int(self.__mPattern[self.__mCurrent][0])
        self.__mLength = int(self.__mPattern[self.__mCurrent][1])
        
        if direction == MoveDirection.UP:
            self.__mTarget.Set(self.mBody.position.x, self.mBody.position.y - self.__mLength)
        elif direction == MoveDirection.RIGHT:
            self.__mTarget.Set(self.mBody.position.x + self.__mLength, self.mBody.position.y)
        elif direction == MoveDirection.DOWN:
            self.__mTarget.Set(self.mBody.position.x, self.mBody.position.y + self.__mLength)
        else:
            self.__mTarget.Set(self.mBody.position.x - self.__mLength, self.mBody.position.y)
            
    speed = property(lambda self: self.__mSpeed)
            