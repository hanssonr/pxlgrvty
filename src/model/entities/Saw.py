from Box2D import b2Vec2
from Enemy import Enemy, EnemyShape
from model.Direction import MoveDirection


class Saw(Enemy):
    
    __mCurrent = None
    __mTarget = None
    mSpeed = None
    
    def __init__(self, physworld, pos, movepattern, radius, speed):
        self.__mTarget = b2Vec2(0,0)
        self.__mCurrent = 0
        self.mPattern = movepattern
        self.mSpeed = speed
        super(Saw, self).__init__(physworld, pos, b2Vec2(radius, radius), EnemyShape.CIRCLE, self)
        self.calculateTarget()
    
    
    def update(self, delta):
        if (self.mBody.position.x >= self.__mTarget.x - 0.01 and self.mBody.position.x <= self.__mTarget.x + 0.01 and
            self.mBody.position.y <= self.__mTarget.y + 0.01 and self.mBody.position.y >= self.__mTarget.y - 0.01):
            self.__mCurrent = 0 if self.__mCurrent + 1 > len(self.mPattern)-1 else self.__mCurrent + 1
            self.calculateTarget()
        else:
            direction = self.__mTarget.copy() - self.mBody.position.copy()
            direction.Normalize()
            velocity = direction * self.mSpeed
            self.mBody.linearVelocity = velocity
        
    def calculateTarget(self):
        direction = int(self.mPattern[self.__mCurrent][0])
        amount = int(self.mPattern[self.__mCurrent][1])
        
        if direction == MoveDirection.UP:
            self.__mTarget.Set(self.mBody.position.x, self.mBody.position.y - amount)
        elif direction == MoveDirection.RIGHT:
            self.__mTarget.Set(self.mBody.position.x + amount, self.mBody.position.y)
        elif direction == MoveDirection.DOWN:
            self.__mTarget.Set(self.mBody.position.x, self.mBody.position.y + amount)
        else:
            self.__mTarget.Set(self.mBody.position.x - amount, self.mBody.position.y)
            