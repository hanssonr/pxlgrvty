from Resources import *
from libs.Sprite import *
from model.entities.Box import *
from model.entities.Crystal import Crystal
from libs.Animation import Animation
import random

class ObjectRender(object):
    
    __mCrystalAnimations = None
    __mCrystalTimers = None
    
    def __init__(self, camera, objects):
        self.__mCrystalTimers = {}
        self.__mCrystalAnimations = {}
        self.mCamera = camera
        self.box = Sprite(Resources.getInstance().mBox)
        self.levelUpdate(objects)
        
        
    def render(self, delta):
        for obj in self.mObjects:
            
            viewpos = self.mCamera.getViewCoords(b2Vec2(obj.position.x - obj.size.x/2, obj.position.y - obj.size.y/2))
            if isinstance(obj, Box):
                self.box.setSize(self.mCamera.getScaledSize(1.04, 1.04))
                self.box.draw(viewpos)
            elif isinstance(obj, Crystal):
                if obj.alive:
                    anim = self.__mCrystalAnimations[obj.id]
                    if anim.isAnimationDone():
                        self.__mCrystalTimers[obj.id] -= delta
                        if self.__mCrystalTimers[obj.id] < 0:
                            anim.reset()
                            self.__mCrystalTimers[obj.id] = random.uniform(2,4) + obj.id

                    anim.draw(delta, viewpos)
                
    
    def levelUpdate(self, objects):
        self.__mCrystalAnimations = {}
        self.__mCrystalTimers = {}
        self.mObjects = objects
        
        for obj in objects:
            if isinstance(obj, Crystal):
                self.__mCrystalAnimations[obj.id] = Animation(Resources.getInstance().mCrystal,  5, 1, 0.6, self.mCamera.getScaledSize(obj.size.x, obj.size.y), False, True)
                self.__mCrystalTimers[obj.id] = random.uniform(2,4)
        
                
        