"""
Enemyclass for moving spikeboxes

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

from model.entities.Enemy import Enemy, EnemyShape
from Box2D import b2Vec2, b2Vec2_zero

class SpikeBox(Enemy):

    __SIZE = b2Vec2(0.5, 0.5)
    mVelocity = b2Vec2(0,0)
    __mTarget = None
    mSpeed = 0.0
    __mLength = None

    #For directionchange
    isTouching = 0
    __dirChange = False
    __stuckTimer = 0


    def __init__(self, physworld, startpos, endpos, delay, speed):
        self.mSpeed = speed
        self.__mStartPos = b2Vec2(startpos[0] + 0.5, startpos[1] + 0.5)
        self.__mEndPos = b2Vec2(endpos[0] + 0.5, endpos[1] + 0.5)
        self.__mTarget = self.__mEndPos.copy()
        self.__mDelay = delay
        super(SpikeBox, self).__init__(physworld, self.__mStartPos, self.__SIZE, EnemyShape.POLYGON, self)
        self.__mLength = (self.__mTarget.copy() - self.mBody.position.copy()).length

    def update(self, delta):

        #touching something, change direction
        if self.isTouching > 0:
            if self.__dirChange == False:
                self.__changeDirection()

        #hack for getting stuck
        if self.__dirChange:
            self.__stuckTimer += delta

            if self.__stuckTimer > 0.1:
                self.__stuckTimer = 0
                self.__dirChange = False

        if self.__mDelay > 0:
            self.__mDelay -= delta
        else:

            #length to target
            if self.__mLength == 0:
                self.__changeDirection()
            else:
                #calculate direction
                direction = self.__mTarget.copy() - self.mBody.position.copy()
                direction.Normalize()
                velocity = direction * self.mSpeed

                #length smaller than velocity * delta, calculate required velocity
                if self.__mLength - velocity.copy().length * delta > 0:
                    self.__mLength -= velocity.copy().length * delta
                else:
                    velocity = direction * (self.__mLength / delta)
                    self.__mLength = 0

                if velocity == b2Vec2_zero:
                    self.__changeDirection()

                self.mBody.linearVelocity = velocity


    def __changeDirection(self):
        if self.__dirChange == False:
            self.__dirChange = True
            self.__mTarget = self.__mEndPos if self.__mTarget.x == self.__mStartPos.x and self.__mTarget.y == self.__mStartPos.y else self.__mStartPos
            self.__mLength = (self.__mTarget.copy() - self.mBody.position.copy()).length

    def touch(self):
        self.isTouching += 1

    def endtouch(self):
        self.isTouching -= 1
