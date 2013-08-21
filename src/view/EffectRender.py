"""
Class that draws all effects

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

from Resources import Resources
from libs.Animation import Animation
import random

class EffectRender(object):
    
    mEffects = None
    
    def __init__(self, camera):
        self.mEffects = []
        self.mCamera = camera
        self.blood = Animation(Resources.getInstance().mBlood, 5, 1, 0, self.mCamera.getScaledSize(1,1), False, False)
            
    def render(self, delta):
        remove = []

        for fx in self.mEffects:
            if fx.isAlive():
                for particle in fx.particles:
                    if particle.alive:
                        viewpos = self.mCamera.getViewCoords(particle.position)
                        random.seed(particle.mSize.x)
                        self.blood.freeze(random.randint(0, 4), 0)
                        self.blood.setSize(self.mCamera.getScaledSize(particle.mSize.x, particle.mSize.y))
                        self.blood.draw(delta, viewpos)
            else:
                remove.append(fx)
        
        for fx in remove:
            self.mEffects.remove(fx)
    
    def addFx(self, fx):
        self.mEffects.append(fx)