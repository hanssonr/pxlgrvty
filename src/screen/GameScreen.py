import pygame
from controller.Input import Input
from model.WorldModel import WorldModel
from model.Camera import Camera
from view.WorldRender import WorldRender
from libs.Pgl import Pgl
from observer.Observers import *
import LevelScreen, LevelTimeScreen, model.Time as Time
from Resources import *

class GameScreen(object):
    
    mWorld = None
    mCamera = None
    mWorldRender = None
    
    def __init__(self, game, lvl):
        pygame.mouse.set_visible(False)
        #pygame.mixer.music.play(0)
        self.mGame = game
        self.mLuObs = LevelupdateObserver()
        self.mFxObs = FXObserver()
        self.mCamera = Camera(Pgl.width, Pgl.height)
        self.mWorld = WorldModel(self.mCamera, self.mLuObs, self.mFxObs, lvl)
        if lvl > self.mWorld.level.mMaxLevels: self.goBack()
        self.mWorldRender = WorldRender(self.mWorld, self.mCamera)
        self.mGame.input = Input(self, self.mWorld, self.mCamera)
        
        self.mLuObs.addListener(self.mWorldRender)
        self.mFxObs.addListener(self.mWorldRender)
    
    def update(self, delta):
        self.mCamera.update(delta, self.mWorld.mEntityToFollow.position, self.mWorld.level.mWidth, self.mWorld.level.mHeight)
        self.mWorld.update(delta)
        
        if self.mWorld.mLevelDone:
            self.mGame.setScreen(LevelTimeScreen.LevelTimeScreen(self.mGame, self.mWorld.level.mCurrentLevel, Time.Time.convertToTimeFormat(self.mWorld.mTimer)))
    
    def render(self, delta):
        self.mWorldRender.render(delta)

    def goBack(self):
        self.mWorld = None
        self.mWorldRender = None
        self.mGame.setScreen(LevelScreen.LevelScreen(self.mGame))