from libs.Sprite import Sprite
from Resources import Resources
from libs.Pgl import *
import pygame

class BackgroundRender(object):
    
    def __init__(self, camera, level):
        self.mCamera = camera
        self.levelUpdate(level)
    
    
    def render(self, delta):
        Pgl.app.surface.fill(self.bgColor)
        pos = self.mCamera.getScaledSize(3 - self.mCamera.displacement.x / 6, 2 - self.mCamera.displacement.y / 2.5)
        self.bg.draw(pos)
        
    
    def levelUpdate(self, level):
        self.bg = Sprite(pygame.image.load("assets/gfx/%s" % level.mBackground).convert())
        self.bg.setSize(self.mCamera.getScaledSize(5,5))
        self.bgColor = level.mBackgroundcolor
    