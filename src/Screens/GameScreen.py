import pygame
from Libs.Pgl import *
from Controller.Input import *
from Model.WorldModel import * 
from View.WorldRender import *
from Model.Camera import *

class GameScreen(object):
    
    mWorld = None
    mCamera = None
    mWorldRender = None
    
    def __init__(self, game):
        print "GameScreen init"
        self.mGame = game
        
        self.mWorld = WorldModel()
        self.mCamera = Camera(Pgl.width, Pgl.height)
        self.mWorldRender = WorldRender(self.mWorld, self.mCamera)
        game.setInput(Input(self.mWorld, self.mCamera))
    
    def update(self, delta):
        self.mWorld.update(delta)
    
    def render(self, delta):
        self.mWorldRender.render(delta)