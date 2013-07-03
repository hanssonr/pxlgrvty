from Resources import *
from libs.Sprite import *
from model.entities.Box import *

class ObjectRender(object):
    
    def __init__(self, camera, objects):
        self.mCamera = camera
        self.mObjects = objects
        
        self.box = Sprite(Resources.getInstance().mBox)
        
        
    def render(self, delta):
        
        for obj in self.mObjects:
            self.box.setSize(self.mCamera.getScaledSize(obj.size.x, obj.size.y)) 
            viewpos = self.mCamera.getViewCoords(b2Vec2(obj.position.x - obj.size.x/2, obj.position.y - obj.size.y/2))
            if isinstance(obj, Box):
                self.box.draw(viewpos)
                
        