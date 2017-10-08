"""
Laser Enemy, takes two positions, triggertime and a firingtime

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

from model.entities.Enemy import *
from Box2D import b2Vec2
from model.Direction import Facing
import math

class Laser(Enemy):

    mLaserTime = 0
    mWarming = False
    mFiring = False

    def __init__(self, physworld, spos, epos, delay, triggertime, firetime):
        self.physworld = physworld
        self.mStartPos = spos
        self.mEndPos = epos
        self.mDelay = delay
        self.mTriggerTime = triggertime
        self.mFireTime = firetime

        vdir = epos.copy() - spos.copy()
        size = vdir.copy()
        vdir.Normalize()

        self.mStartRot = math.degrees(math.atan2(vdir.y, vdir.x))

        self.mStartFacing = Facing.convertFromVector2(vdir)
        self.mEndFacing = Facing.convertFromVector2(-vdir)
        pos = (spos + epos) / 2.0
        super(Laser, self).__init__(physworld, pos, size, EnemyShape.LINE, self)

        if self.mFireTime < 0:
            self.mBody.active = True
            self.mFiring = True
        else:
            self.mBody.active = False

    def update(self, delta):
        if self.mDelay > 0:
            self.mDelay -= delta
        else:
            if self.mFireTime < 0:
                return

            self.mLaserTime += delta

            if self.mFiring:
                if self.mLaserTime > self.mFireTime:
                    self.mLaserTime = 0
                    self.mFiring = False
                    self.mBody.active = False
            else:
                if self.mLaserTime > self.mTriggerTime - 0.5 and self.mWarming == False:
                    self.mWarming = True

                if self.mLaserTime > self.mTriggerTime:
                    self.mLaserTime = 0
                    self.mFiring = True
                    self.mWarming = False
                    self.mBody.active = True
