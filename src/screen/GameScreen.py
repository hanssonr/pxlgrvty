import pygame
from controller.Input import Input
from model.WorldModel import WorldModel
from model.Camera import Camera
from view.WorldRender import WorldRender
from libs.Pgl import Pgl

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