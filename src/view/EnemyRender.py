from Resources import *
from libs.Sprite import *
from model.entities.SpikeBox import SpikeBox
from Box2D import b2Vec2

class EnemyRender(object):
    
    def __init__(self, camera, enemies):
        self.mCamera = camera
        self.mEnemies = enemies
        
        #TODO: load all enemies from spritesheet(Animation)
        self.spikebox = Sprite(Resources.getInstance().mSpikeBox)
        
        
    def render(self, delta):
        
        for e in self.mEnemies:
            self.spikebox.setSize(self.mCamera.getScaledSize(e.size.x, e.size.y)) 
            viewpos = self.mCamera.getViewCoords(b2Vec2(e.position.x - e.size.x/2, e.position.y - e.size.y/2))
            if isinstance(e, SpikeBox):
                self.spikebox.draw(viewpos)
    
    def levelUpdate(self, enemies):
        self.mEnemies = enemies
                
        