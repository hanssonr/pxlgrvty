import pygame
from Libs.Pgl import *
from DebugDraw import *


class WorldRender(object):
    
    def __init__(self, world, camera):
        self.mWorld = world
        self.mCamera = camera
           
        #debugrender only
        self.debug = DebugDraw(self.mCamera)
        self.mWorld.physWorld.renderer = self.debug
        self.debug.AppendFlags(self.debug.e_shapeBit)
    
    def render(self, delta):
        Pgl.app.surface.fill((0,0,0))
        self.mWorld.physWorld.DrawDebugData()
        pygame.display.flip()