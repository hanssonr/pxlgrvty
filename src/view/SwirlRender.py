"""
Class that draws the endwarp

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

from Resources import Resources
from libs.Animation import Animation

class SwirlRender(object):
    
    __swirlActivation = None
    
    def __init__(self, camera, level):
        self.__swirlActivation = False
        self.mLevel = level
        self.mCamera = camera
        self.swirl = Animation(Resources.getInstance().mSwirlSheet, 3, 2, 0.45, self.mCamera.getScaledSize(1,1))
        self.swirl.setLooping(False)       
    
    def render(self, delta):
        if self.mCamera.isInFrustum(self.mLevel.mEndPos.x, self.mLevel.mEndPos.y):
            viewpos = self.mCamera.getViewCoords(self.mLevel.mEndPos)
    
            if not self.mLevel.mSwirlActive:
                self.swirl.freeze(0, 0)
            else:
                if not self.__swirlActivation:
                    self.swirl.continueAnimation()
                    if self.swirl.isAnimationDone():
                        self.__swirlActivation = True
                        self.swirl.setLooping(True)
                        self.swirl.gotoRow(1)
                    
            self.swirl.draw(delta, viewpos)
        
    
    def levelUpdate(self):
        self.__swirlActivation = False
        self.swirl.setLooping(False)
        self.swirl.reset()
        