import pygame
from libs.Pgl import *
from DebugDraw import *
from view.TileRender import TileRender
from view.PlayerRender import PlayerRender
from Resources import *
from view.ObjectRender import ObjectRender
from view.EnemyRender import EnemyRender
from view.SwirlRender import SwirlRender
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
        self.tileRender = TileRender(self.mCamera, self.mWorld.level.mTiles, self.mWorld.level.mCurrentTileset)
        self.enemyRender = EnemyRender(self.mCamera, self.mWorld.level.mEnemies)
        self.swirlRender = SwirlRender(self.mCamera, self.mWorld.level)
    
    def render(self, delta):
        Pgl.app.surface.fill((60,59,77))
        
        if self.mWorld.DEBUG:
            self.mWorld.physWorld.DrawDebugData()
            self.enemyRender.render(delta)
        else:
            self.objectRender.render(delta)
            self.swirlRender.render(delta)
            self.enemyRender.render(delta)
            self.playerRender.render(delta)
            self.tileRender.render(delta)
            
            
            
        self.label = Resources.getInstance().getScaledFont(20).render("FPS: %d" % (Pgl.clock.get_fps()), 1, (255,255,255))
        Pgl.app.surface.blit(self.label, (10,10))
        
        self.time = Resources.getInstance().getScaledFont(self.mCamera.scale.x).render("%.2f" % self.mWorld.mTimer, 0, (255, 255, 255))
        Pgl.app.surface.blit(self.time, (self.mCamera.getScaledSize(Camera.CAMERA_WIDTH / 2.2, Camera.CAMERA_HEIGHT - 1)))
    

    def levelChanged(self, level):
        self.tileRender.levelUpdate(level.mTiles, level.mCurrentTileset)
        self.objectRender.levelUpdate(level.mObjects)
        self.enemyRender.levelUpdate(level.mEnemies)
        self.swirlRender.levelUpdate()