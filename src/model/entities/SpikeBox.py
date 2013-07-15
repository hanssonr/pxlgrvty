from Enemy import Enemy
from Box2D import b2Vec2

class SpikeBox(Enemy):
    
    __SIZE = b2Vec2(0.5, 0.5)
    __mVelocity = b2Vec2(0,0)
    __mDirection = None
    __mSpeed = 3.0
    
    #For directionchange
    __isTouching = 0
    __dirChange = True
    
    
    def __init__(self, physworld, startpos, direction, delay):
        self.__mStartPos = b2Vec2(startpos[0] + self.__SIZE.x / 2, startpos[1] + self.__SIZE.y / 2) 
        self.__mDirection = direction
        self.__mDelay = delay
        
        super(SpikeBox, self).__init__(physworld, self.__mStartPos, self.__SIZE, self)
    
    def update(self, delta):        
        if self.__mDelay > 0:
            self.__mDelay -= delta
        else:
            self.__mVelocity.Set(self.__mDirection.x * self.__mSpeed, self.__mDirection.y * self.__mSpeed)    
            self.mBody.linearVelocity = self.__mVelocity
    
    def __changeDirection(self):
        self.__mDirection *= -1
            
    def touch(self):
        if self.__isTouching == 0:
            self.__changeDirection()
            
        self.__isTouching += 1
    
    def endtouch(self):
        self.__isTouching -= 1