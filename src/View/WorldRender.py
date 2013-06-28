import pygame
from libs.Pgl import *
from DebugDraw import *
from view.TileRender import TileRender


class WorldRender(object):
    
    def __init__(self, world, camera):
        self.mWorld = world
        self.mCamera = camera
           
        #debugrender only
        self.debug = DebugDraw(self.mCamera)
        self.mWorld.physWorld.renderer = self.debug
        self.debug.AppendFlags(self.debug.e_shapeBit)
        
        self.tileRender = TileRender(self.mCamera, self.mWorld.level.mMap)
        
        #fps
        self.font = pygame.font.SysFont('mono', 36)
    
    def render(self, delta):
        Pgl.app.surface.fill((0,0,0))
        self.mWorld.physWorld.DrawDebugData()
    
        self.tileRender.render(delta)
        
        self.label = self.font.render("FPS: %d" % (Pgl.clock.get_fps()), 1, (255,255,255))
        Pgl.app.surface.blit(self.label, (10,10))