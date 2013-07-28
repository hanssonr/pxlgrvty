from Box2D import b2Vec2
from Enemy import Enemy, EnemyShape
from model.Direction import MoveDirection


class Saw(Enemy):
    
    mCurrent = None
    mTarget = None
    mSpeed = None
    
    def __init__(self, physworld, pos, movepattern, radius, speed):
        self.mTarget = b2Vec2(0,0)
        self.mCurrent = 0
        self.mPattern = movepattern
        self.mSpeed = speed
        super(Saw, self).__init__(physworld, pos, b2Vec2(radius, radius), EnemyShape.CIRCLE, self)
        self.calculateTarget()
    
    
    def update(self, delta):
        if (self.mBody.position.x >= self.mTarget.x - 0.01 and self.mBody.position.x <= self.mTarget.x + 0.01 and
            self.mBody.position.y <= self.mTarget.y + 0.01 and self.mBody.position.y >= self.mTarget.y - 0.01):
            self.mCurrent = 0 if self.mCurrent + 1 > len(self.mPattern)-1 else self.mCurrent + 1
            self.calculateTarget()
        else:
            direction = self.mTarget.copy() - self.mBody.position.copy()
            direction.Normalize()
            velocity = direction * self.mSpeed
            self.mBody.linearVelocity = velocity
        
    def calculateTarget(self):
        direction = int(self.mPattern[self.mCurrent][0])
        amount = int(self.mPattern[self.mCurrent][1])
        
        if direction == MoveDirection.UP:
            self.mTarget.Set(self.mBody.position.x, self.mBody.position.y - amount)
        elif direction == MoveDirection.RIGHT:
            self.mTarget.Set(self.mBody.position.x + amount, self.mBody.position.y)
        elif direction == MoveDirection.DOWN:
            self.mTarget.Set(self.mBody.position.x, self.mBody.position.y + amount)
        else:
            self.mTarget.Set(self.mBody.position.x - amount, self.mBody.position.y)
            