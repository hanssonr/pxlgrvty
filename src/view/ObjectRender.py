from Resources import *
from libs.Sprite import *
from model.entities.Box import *
from model.entities.Nugget import Nugget
from libs.Animation import Animation

class ObjectRender(object):
    
    __mNuggetAnimations = {}
    
    def __init__(self, camera, objects):
        self.mCamera = camera
        self.box = Sprite(Resources.getInstance().mBox)
        self.levelUpdate(objects)
        
        
    def render(self, delta):
        
        for obj in self.mObjects:
            
            viewpos = self.mCamera.getViewCoords(b2Vec2(obj.position.x - obj.size.x/2, obj.position.y - obj.size.y/2))
            if isinstance(obj, Box):
                self.box.setSize(self.mCamera.getScaledSize(1.04, 1.04)) 
                self.box.draw(viewpos)
            elif isinstance(obj, Nugget):
                self.__mNuggetAnimations[obj.id].draw(delta, viewpos)
                
    
    def levelUpdate(self, objects):
        self.mObjects = objects
        
        for obj in objects:
            if isinstance(obj, Nugget):
                self.__mNuggetAnimations[obj.id] = Animation(Resources.getInstance().mNugget,  4, 1, 0.4, self.mCamera.getScaledSize(obj.size.x, obj.size.y))
        
                
        