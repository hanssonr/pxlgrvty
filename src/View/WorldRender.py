import pygame
from libs.Pgl import *
from DebugDraw import *
from view.TileRender import TileRender
from view.PlayerRender import PlayerRender
from Resources import *
from view.ObjectRender import ObjectRender
from view.EnemyRender import EnemyRender
from view.SwirlRender import SwirlRender
from view.EffectRender import EffectRender
from view.BackgroundRender import BackgroundRender
from observer.Observers import *
from model.Time import Time
from libs.Sprite import Sprite

class WorldRender(object):
    
    def __init__(self, world, camera):
        self.mWorld = world
        self.mCamera = camera
        
        self.ui = Sprite(Resources.getInstance().mUI)
        self.ui.setSize(self.mCamera.getScaledSize(4,1))

        self.timesize = Resources.getInstance().getScaledFont(self.mCamera.scale.x).size("00:00:00")
        
        #debugrender only
        self.debug = DebugDraw(self.mCamera)
        self.mWorld.physWorld.renderer = self.debug
        self.debug.AppendFlags(self.debug.e_shapeBit)
        
        self.objectRender = ObjectRender(self.mCamera, self.mWorld.level.mObjects)
        self.playerRender = PlayerRender(self.mCamera, self.mWorld.player)
        self.tileRender = TileRender(self.mCamera, self.mWorld.level.mTiles, self.mWorld.level.mCurrentTileset)
        self.enemyRender = EnemyRender(self.mCamera, self.mWorld.level.mEnemies)
        self.swirlRender = SwirlRender(self.mCamera, self.mWorld.level)
        self.fxRender = EffectRender(self.mCamera)
        self.bgRender = BackgroundRender(self.mCamera, self.mWorld.level)
    
    def render(self, delta):
        self.bgRender.render(delta)
        
        if self.mWorld.DEBUG:
            self.mWorld.physWorld.DrawDebugData()
            self.enemyRender.render(delta)
        else:
            self.objectRender.render(delta)
            self.swirlRender.render(delta)
            self.enemyRender.render(delta)
            self.playerRender.render(delta)
            self.tileRender.render(delta)
            self.fxRender.render(delta)
        
        uipos =  self.mCamera.getScaledSize(Camera.CAMERA_WIDTH / 2.0 - 2, Camera.CAMERA_HEIGHT - 1)
        self.ui.draw(b2Vec2(uipos.x, uipos.y))
            
        self.label = Resources.getInstance().getScaledFont(20).render("FPS: %d" % (Pgl.clock.get_fps()), 1, (255,255,255))
        Pgl.app.surface.blit(self.label, (10,10))
        
        self.time = Resources.getInstance().getScaledFont(self.mCamera.scale.x).render(Time.convertToTimeString(self.mWorld.mTimer), 0, (255, 255, 255))
        Pgl.app.surface.blit(self.time, (self.mCamera.getScaledSize(Camera.CAMERA_WIDTH / 2.0 - (self.timesize[0] / 2.0) / self.mCamera.scale.x, Camera.CAMERA_HEIGHT - ((10 +self.timesize[1]) / self.mCamera.scale.y))))
    

    "implementing LevelupdateListener"
    def levelChanged(self, level):
        self.tileRender.levelUpdate(level.mTiles, level.mCurrentTileset)
        self.objectRender.levelUpdate(level.mObjects)
        self.enemyRender.levelUpdate(level.mEnemies)
        self.swirlRender.levelUpdate()
        self.bgRender.levelUpdate(level)
    
    "implementing FXListener"    
    def addFx(self, fx):
        self.fxRender.addFx(fx)