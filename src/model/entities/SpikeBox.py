from Enemy import Enemy, EnemyShape
from Box2D import b2Vec2

class SpikeBox(Enemy):
    
    __SIZE = b2Vec2(0.5, 0.5)
    mVelocity = b2Vec2(0,0)
    __mTarget = None
    mSpeed = 0.0
    
    #For directionchange
    isTouching = 0
    __dirChange = False
    __stuckTimer = 0.1
    
    
    def __init__(self, physworld, startpos, endpos, delay, speed):
        self.mSpeed = speed
        self.__mStartPos = b2Vec2(startpos[0] + 0.5, startpos[1] + 0.5) 
        self.__mEndPos = b2Vec2(endpos[0] + 0.5, endpos[1] + 0.5)
        self.__mTarget = self.__mEndPos.copy()
        self.__mDelay = delay
        
        super(SpikeBox, self).__init__(physworld, self.__mStartPos, self.__SIZE, EnemyShape.POLYGON, self)
    
    def update(self, delta):     
        if self.isTouching > 0:
            self.__changeDirection()
        
        #hack for getting stuck
        if self.__dirChange:
            self.__stuckTimer -= delta
            
            if self.__stuckTimer < 0:
                self.__stuckTimer = 0.2
                self.__dirChange = False
        
        if self.__mDelay > 0:
            self.__mDelay -= delta
        else:
            if (self.mBody.position.x >= self.__mTarget.x - 0.01 and self.mBody.position.x <= self.__mTarget.x + 0.01 and
                self.mBody.position.y <= self.__mTarget.y + 0.01 and self.mBody.position.y >= self.__mTarget.y - 0.01):
                self.__changeDirection()
            else:
                direction = self.__mTarget.copy() - self.mBody.position.copy()
                direction.Normalize()
                velocity = direction * self.mSpeed
                self.mBody.linearVelocity = velocity
    
    def __changeDirection(self):
        if self.__dirChange == False:
            self.__dirChange = True
            self.__mTarget = self.__mEndPos if self.__mTarget.x == self.__mStartPos.x and self.__mTarget.y == self.__mStartPos.y else self.__mStartPos
            
    def touch(self):
        self.isTouching += 1 
        
    def endtouch(self):
        self.isTouching -= 1
