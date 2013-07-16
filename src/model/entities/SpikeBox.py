from Enemy import Enemy
from Box2D import b2Vec2

class SpikeBox(Enemy):
    
    __SIZE = b2Vec2(0.5, 0.5)
    __mVelocity = b2Vec2(0,0)
    __mDirection = None
    __mSpeed = 0.0
    
    #For directionchange
    isTouching = 0
    __dirChange = False
    __stuckTimer = 0.1
    
    
    def __init__(self, physworld, startpos, direction, delay, speed):
        self.__mSpeed = speed
        self.__mStartPos = b2Vec2(startpos[0] + self.__SIZE.x / 2, startpos[1] + self.__SIZE.y / 2) 
        self.__mDirection = direction
        self.__mDelay = delay
        
        super(SpikeBox, self).__init__(physworld, self.__mStartPos, self.__SIZE, self)
    
    def update(self, delta):     
        if self.isTouching > 0:
            self.mBody.mass = 1
            self.__changeDirection()
        else:
            self.mBody.mass = 10000
        
        #hack for getting stuck
        if self.__dirChange:
            self.__stuckTimer -= delta
            
            if self.__stuckTimer < 0:
                self.__stuckTimer = 0.2
                self.__dirChange = False
        
        if self.__mDelay > 0:
            self.__mDelay -= delta
        else:
            self.__mVelocity.Set(self.__mDirection.x * self.__mSpeed, self.__mDirection.y * self.__mSpeed)    
            self.mBody.linearVelocity = self.__mVelocity
    
    def __changeDirection(self):
        if self.__dirChange == False:
            self.__dirChange = True
            self.__mDirection *= -1
            
    def touch(self):
        self.isTouching += 1 
        
    def endtouch(self):
        self.isTouching -= 1
