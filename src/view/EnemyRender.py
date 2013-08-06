from Resources import *
from libs.Sprite import *
from model.Direction import Facing
from model.entities.SpikeBox import SpikeBox
from model.entities.Spike import Spike
from model.entities.Saw import Saw
from libs.Animation import Animation
from Box2D import b2Vec2

class EnemyRender(object):
    
    def __init__(self, camera, enemies):
        self.mCamera = camera
        self.mEnemies = enemies
        
        self.spikebox = Animation(Resources.getInstance().mSpikeBox, 1, 1, 0, self.mCamera.getScaledSize(1,1), False)
        self.spike = Animation(Resources.getInstance().mSpike, 1, 1, 0, self.mCamera.getScaledSize(1,1), False)
        self.saw = Animation(Resources.getInstance().mSaw, 2, 1, 0.1, self.mCamera.getScaledSize(1,1))
        
        
    def render(self, delta):
        
        for e in self.mEnemies:
            if self.mCamera.isInFrustum(e.position.x, e.position.y):
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
                    toDraw = self.saw
                
                viewpos = self.mCamera.getViewCoords(b2Vec2(e.position.x - (size.x)/2, e.position.y - (size.y)/2))
                toDraw.setSize(self.mCamera.getScaledSize(size.x, size.y))
                toDraw.draw(delta, viewpos)
    
    def levelUpdate(self, enemies):
        self.mEnemies = enemies
                
        