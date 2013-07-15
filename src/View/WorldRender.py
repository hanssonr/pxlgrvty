import pygame
from libs.Pgl import *
from DebugDraw import *
from view.TileRender import TileRender
from view.PlayerRender import PlayerRender
from Resources import *
from view.ObjectRender import ObjectRender
from view.EnemyRender import EnemyRender
from observer.Observers import *

class WorldRender(LevelupdateListener):
    
    def __init__(self, world, camera):
        self.mWorld = world
        self.mCamera = camera
           
        #debugrender only
        self.debug = DebugDraw(self.mCamera)
        self.mWorld.physWorld.renderer = self.debug
        self.debug.AppendFlags(self.debug.e_shapeBit)
        
        self.objectRender = ObjectRender(self.mCamera, self.mWorld.level.mObjects)
        self.playerRender = PlayerRender(self.mCamera, self.mWorld.player)
        self.tileRender = TileRender(self.mCamera, self.mWorld.level.mTiles)
        self.enemyRender = EnemyRender(self.mCamera, self.mWorld.level.mEnemies)
    
    def render(self, delta):
        Pgl.app.surface.fill((255,255,255))
        
        if self.mWorld.DEBUG:
            self.mWorld.physWorld.DrawDebugData()
        else:
            self.tileRender.render(delta)
            self.objectRender.render(delta)
        
        self.playerRender.render(delta)
        self.enemyRender.render(delta)
        
        
        self.label = Resources.getInstance().mFpsFont.render("FPS: %d" % (Pgl.clock.get_fps()), 1, (0,0,0))
        Pgl.app.surface.blit(self.label, (10,10))
    

    def levelChanged(self, level):
        self.tileRender.levelUpdate(level.mTiles)
        self.objectRender.levelUpdate(level.mObjects)
        self.enemyRender.levelUpdate(level.mEnemies)