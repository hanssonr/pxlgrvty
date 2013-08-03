from libs.Pgl import *
from Resources import Resources
from model.Camera import Camera
from Box2D import b2Vec2

class EndScreen(object):
    
    def __init__(self, game):
        self.mCamera = Camera(Pgl.width, Pgl.height)
        self.titleFont = Resources.getInstance().getScaledFont(self.mCamera.scale.x * 2.0)
        self.modelsize = self.mCamera.getModelCoords(b2Vec2(Pgl.width, Pgl.height))
    
    
    def update(self, delta):
        pass
    
    def render(self, delta):
        Pgl.app.surface.fill((167,74,20))
        
        title = self.titleFont.render("the end", 0, (255,255,255))
        size = self.titleFont.size("the end")
        titlepos = self.mCamera.getViewCoords(b2Vec2(self.modelsize.x / 2.0, self.modelsize.y / 2.0))
        Pgl.app.surface.blit(title, (titlepos.x - size[0] / 2.0, titlepos.y - size[1] / 2.0))