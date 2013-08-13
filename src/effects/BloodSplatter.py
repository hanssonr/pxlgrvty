from Particle import Particle
from Box2D import b2Vec2
import random

class BloodSplatter(object):
    
    __mNrOfParticles = 150
    __mParticles = None
    
    def __init__(self, physworld, gravity, pos):
        self.mWorld = physworld
        self.__mParticles = []
        
        for x in range(self.__mNrOfParticles):
            rs = random.uniform(0.03, 0.12)
            particle = Particle(physworld, -gravity/4.0, b2Vec2(rs, rs), min(rs * 10, 1), pos)
            randDir = b2Vec2(random.uniform(-0.5, 0.5), random.uniform(-0.8, 0.2))
            randDir.Normalize()
            particle.mVelocity = randDir * (particle.mSpeed * random.uniform(0.2, 1.5))         
            self.__mParticles.append(particle)
    
    def isAlive(self):
        alive = False
        
        for p in self.__mParticles:
            if p.mIsAlive == True:
                alive = True
                break
        
        return alive
    
    def __getParticles(self):
        return self.__mParticles
    
    particles = property(__getParticles, None)
                                   
            