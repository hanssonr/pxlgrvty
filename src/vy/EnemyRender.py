"""
Class that draws different types of enemies

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

from Resources import *
from libs.Sprite import *
from model.Direction import Facing
from model.entities.SpikeBox import SpikeBox
from model.entities.Spike import Spike
from model.entities.Saw import Saw
from model.entities.Laser import Laser
from libs.Animation import Animation
from Box2D import b2Vec2
import math, random

class EnemyRender(object):
    
    def __init__(self, camera, enemies):
        self.mCamera = camera
        self.levelUpdate(enemies)
        self.spikebox = Animation(Resources.getInstance().mSpikeBox, 1, 1, 0, self.mCamera.getScaledSize(1,1), False)
        self.spike = Animation(Resources.getInstance().mSpike, 1, 1, 0, self.mCamera.getScaledSize(1,1), False)
        self.laser = Animation(Resources.getInstance().mLasermount, 1, 1, 0, self.mCamera.getScaledSize(1,1), False, False)
        
        
    def render(self, delta):
        
        for e in self.mEnemies:
            if self.mCamera.isInFrustum(e.position.x, e.position.y) or isinstance(e, Laser):
                toDraw = None
                size = b2Vec2(e.size.x, e.size.y)
                       
                if isinstance(e, SpikeBox):
                    toDraw = self.spikebox
                elif isinstance(e, Spike):
                    toDraw = self.spike      
                    
                    if e.mFacing == Facing.UP:
                        toDraw.rotate(0)
                        size.Set(1, 0.5)
                        
                    if e.mFacing == Facing.DOWN:
                        toDraw.rotate(180)
                        size.Set(1, 0.5)
                        
                    if e.mFacing == Facing.LEFT:
                        toDraw.rotate(90)
                        size.Set(0.5, 1)
                                  
                    if e.mFacing == Facing.RIGHT:
                        toDraw.rotate(-90)
                        size.Set(0.5, 1)
                        
                        
                elif isinstance(e, Saw):
                    toDraw = self.mSawAnimations[e.mId]
                
                elif isinstance(e, Laser):
                    toDraw = None
                    spos = self.mCamera.getViewCoords(e.mStartPos)
                    epos = self.mCamera.getViewCoords(e.mEndPos)
                    random.seed(e.mId)
                    offset = 2-math.cos((delta * 1.5))
                                     
                    if e.mWarming:
                        pygame.draw.aaline(Pgl.app.surface, (217,115,118), spos * offset, epos * offset, 1)
                    
                    if e.isActive():
                        pygame.draw.line(Pgl.app.surface, (104,28,31), spos * offset, epos * offset, 7)
                        pygame.draw.line(Pgl.app.surface, (158,29,34), spos * offset, epos * offset, 3)
                        pygame.draw.aaline(Pgl.app.surface, (196,196,196), spos * offset, epos * offset, 1)
                    
                    self.laser.setSize(self.mCamera.getScaledSize(0.5,0.5))
                    
                    rot = e.mStartRot
                    
                    if e.mStartFacing == Facing.RIGHT: rot = 270-rot
                    elif e.mStartFacing == Facing.LEFT: rot = 90-rot
                    
                    self.laser.rotate(rot)
                    self.laser.draw(delta, b2Vec2(spos.x - self.laser.getSize().x / 2.0, spos.y - self.laser.getSize().y / 2.0))
                    self.laser.rotate(rot-180)
                    self.laser.draw(delta, b2Vec2(epos.x - self.laser.getSize().x / 2.0, epos.y - self.laser.getSize().y / 2.0))
                    
                
                if toDraw != None:
                    viewpos = self.mCamera.getViewCoords(b2Vec2(e.position.x - size.x/2.0, e.position.y - size.y/2.0))
                    toDraw.setSize(self.mCamera.getScaledSize(size.x, size.y))
                    toDraw.draw(delta, viewpos)
    
    def levelUpdate(self, enemies):
        self.mSawAnimations = {}
        
        for e in enemies:
            if isinstance(e, Saw):
                self.mSawAnimations[e.mId] = Animation(Resources.getInstance().mSaw, 2, 1, min(0.3/e.speed, 0.2), self.mCamera.getScaledSize(1,1))
        
        self.mEnemies = enemies
                
        