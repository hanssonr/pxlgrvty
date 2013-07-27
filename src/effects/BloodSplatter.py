from Particle import Particle
from Box2D import b2Vec2
import random

class BloodSplatter(object):
    
    mNrOfParticles = 150
    mParticles = None
    
    def __init__(self, physworld, gravity, pos):
        self.mWorld = physworld
        self.mParticles = []
        print pos
        
        for x in range(self.mNrOfParticles):
            rs = random.uniform(0.05, 0.12)
            particle = Particle(physworld, b2Vec2(0,1), b2Vec2(rs, rs), min(rs * 10, 1), pos)
            randDir = b2Vec2(random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5))
            randDir.Normalize()
            particle.mVelocity = randDir * (particle.mSpeed * random.uniform(0.2, 1.5))
            self.mParticles.append(particle)
    
    def isAlive(self):
        alive = False
        
        for p in self.mParticles:
            if p.mIsAlive == True:
                alive = True
                break
        
        return alive
    
    def __getParticles(self):
        return self.mParticles
    
    particles = property(__getParticles, None)
                                   
            