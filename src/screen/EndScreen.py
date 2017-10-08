"""
Credits screen

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

from libs.Pgl import *
from Resources import Resources
from Box2D import b2Vec2
from libs.Text import Text
from libs.SoundManager import SoundManager
from screen.BaseMenuScreen import BaseMenuScreen
import screen.MenuScreen, pygame

class EndScreen(BaseMenuScreen):

    def __init__(self, game):
        super(EndScreen, self).__init__(game, False)
        SoundManager.getInstance().playEndMusic()

        #fonts
        self.textFont = Resources.getInstance().getScaledFont(self.mCamera.scale.x * 0.6)
        self.headerFont = Resources.getInstance().getScaledFont(self.mCamera.scale.x)
        self.titleFont = Resources.getInstance().getScaledFont(self.mCamera.scale.x * 2.0)

        self.modelsize = self.mCamera.getModelCoords(b2Vec2(Pgl.width, Pgl.height))
        self.mDone = False
        self.mTimer = 0

        texts = [
                 [self.titleFont, (200,160,160), "pxlgrvty", 0],
                 [self.headerFont, (170,170,170), "Programming:", 25],
                 [self.textFont, (255,255,255), "Rickard Hansson", 0],
                 [self.headerFont, (170,170,170), "Graphics:", 25],
                 [self.textFont, (255,255,255), "Rickard Hansson", 0],
                 [self.headerFont, (170,170,170), "Audio/FX:", 25],
                 [self.textFont, (255,255,255), "Rickard Hansson", 0],
                 [self.headerFont, (170,170,170), "Music:", 25],
                 [self.textFont, (255,255,255), "anamanaguchi - helix nebula", 0],
                 [self.textFont, (255,255,255), "anamanaguchi - video challenge", 0],
                 [self.textFont, (255,255,255), "electric children - spring retrospective", 0],
                 [self.textFont, (255,255,255), "teknoaxe - chiptune does dubstep", 0],
                 [self.textFont, (255,255,255), "roccow - chipho instrumental", 0],
                 [self.textFont, (255,255,255), "sycamore drive - kicks", 0]]

        self.titlepos = self.mCamera.getViewCoords(b2Vec2(self.modelsize.x / 2.0, self.modelsize.y))
        self.text = Text(texts, self.titlepos, 1, Pgl.app.surface)
        self.endtext = self.headerFont.render("thanks for playing!", 1, (170,170,170))
        self.endsize = self.headerFont.size("thanks for playeing!")
        self.endpos = self.mCamera.getViewCoords(b2Vec2(self.modelsize.x/2.0, self.modelsize.y/2.0))


    def update(self, delta):
        if not self.mDone:
            if self.text.mPos.y + self.text.height > 0:
                self.text.mPos.y -= self.mCamera.scale.y * delta / 2.0
            else: self.mDone = True
        else:
            if self.mTimer == 0:
                SoundManager.getInstance().fadeout(4800)

            self.mTimer += delta

            if self.mTimer >= 5:
                self.mGame.setScreen(screen.MenuScreen.MenuScreen(self.mGame))


    def render(self, delta):
        Pgl.app.surface.fill((167,74,20))

        if self.mDone:
            Pgl.app.surface.blit(self.endtext, (self.endpos.x - self.endsize[0]/2.0, self.endpos.y - self.endsize[1]/2.0))
        else:
            self.text.renderleft(delta)

    def mouseClick(self, pos):
        pass

    def mouseOver(self, pos):
        pass

    def keyInput(self, key):
        if key == pygame.K_ESCAPE:
            self.mDone = True
