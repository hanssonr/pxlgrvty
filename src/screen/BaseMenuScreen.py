from libs.Pgl import *
import pygame
from Resources import Resources
from libs.SoundManager import SoundManager
from Box2D import b2Vec2
from libs.Sprite import Sprite
from model.Camera import Camera
from controller.MenuInput import MenuInput
from libs.Animation import Animation

class BaseMenuScreen(object):
    
    def __init__(self, game):
        self.mGame = game
        Pgl.app.setRenderStep(1/60.0)
        SoundManager.getInstance().playMenuMusic()
        pygame.mouse.set_visible(False)
        
        self.mGame.input = MenuInput(self)
        self.mCamera = Camera(Pgl.width, Pgl.height)
        self.modelsize = self.mCamera.getModelCoords(b2Vec2(Pgl.width, Pgl.height))
        
        #fonts
        self.screenFont = Resources.getInstance().getScaledFont(self.mCamera.scale.x / 3.0)
        self.titleFont = Resources.getInstance().getScaledFont(self.mCamera.scale.x * 2.0)
        self.infoFont = Resources.getInstance().getScaledFont(self.mCamera.scale.x / 2)
        
        #graphics
        self.arrow = Sprite(Resources.getInstance().mArrow) 
        self.arrow.setSize(self.mCamera.getScaledSize((self.arrow.getWidth()/float(self.arrow.getHeight())) * 0.5, 0.5))
        self.menubutton = Animation(Resources.getInstance().mMenuButton, 2, 1, 0, self.mCamera.getScaledSize(1, 1), False, False)
        self.levelbutton = Animation(Resources.getInstance().mLevelButton, 2, 1, 0, self.mCamera.getScaledSize(1, 1), False, False)
        self.checkbutton = Animation(Resources.getInstance().mCheckButton, 2, 1, 0, self.mCamera.getScaledSize(1, 1), False, False)
        self.lock = Sprite(Resources.getInstance().mLock)
        self.lock.setSize(self.mCamera.getScaledSize((self.lock.getWidth()/float(self.lock.getHeight())) * 0.2, 0.2))
        
        
    def update(self, delta):
        pos = self.mGame.input.getMousePosition()
        self.arrow.setPosition(pos[0], pos[1])
        self.mouseOver(pos)