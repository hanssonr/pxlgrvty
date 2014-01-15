"""
Class that instantiates the different renderers needed and updates them

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

from view.TileRender import TileRender
from view.PlayerRender import PlayerRender
from view.ObjectRender import ObjectRender
from view.EnemyRender import EnemyRender
from view.SwirlRender import SwirlRender
from view.EffectRender import EffectRender
from view.BackgroundRender import BackgroundRender
from view.UIRender import UIRender
from view.DebugDraw import DebugDraw
from libs.Pgl import *
from Resources import Resources



class WorldRender(object):
    
    def __init__(self, world, camera):
        self.mWorld = world
        self.mCamera = camera
                
        #debugrender only
        self.debug = DebugDraw(self.mCamera)
        self.mWorld.physWorld.renderer = self.debug
        self.debug.AppendFlags(self.debug.e_shapeBit)
        
        #font
        self.fpsfont = Resources.getInstance().getScaledFont(20)
        
        #renders
        self.objectRender = ObjectRender(self.mCamera, self.mWorld.level.mObjects)
        self.playerRender = PlayerRender(self.mCamera, self.mWorld.player)
        self.tileRender = TileRender(self.mCamera, self.mWorld.level)
        self.enemyRender = EnemyRender(self.mCamera, self.mWorld.level.mEnemies)
        self.swirlRender = SwirlRender(self.mCamera, self.mWorld.level)
        self.fxRender = EffectRender(self.mCamera)
        self.bgRender = BackgroundRender(self.mCamera, self.mWorld.level)
        self.uiRender = UIRender(self.mCamera, self.mWorld)     
    
    def render(self, delta):
        self.bgRender.render(delta)
        
        if self.mWorld.DEBUG:
            self.enemyRender.render(delta)
            self.mWorld.physWorld.DrawDebugData()
        else:
            self.objectRender.render(delta)
            self.swirlRender.render(delta)
            self.enemyRender.render(delta)
            self.playerRender.render(delta)
            self.tileRender.render(delta)
            self.fxRender.render(delta)
            self.uiRender.render(delta)
            
        self.label = self.fpsfont.render("FPS: %d" % (Pgl.clock.get_fps()), 1, (255,255,255))
        Pgl.app.surface.blit(self.label, (10,10))
    

    #LevelupdateListener
    def levelChanged(self, level):
        self.tileRender.levelUpdate(level)
        self.objectRender.levelUpdate(level.mObjects)
        self.enemyRender.levelUpdate(level.mEnemies)
        self.swirlRender.levelUpdate()
        self.bgRender.levelUpdate(level)
    
    #FXListener    
    def addFx(self, fx):
        self.fxRender.addFx(fx)