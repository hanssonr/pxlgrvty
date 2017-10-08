"""
A screen that shows all the levels available in the game and renders button for em
If the level is locked render a lock and make it unclickable

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

from libs.Pgl import *
from Box2D import b2Vec2
import os, screen.MenuScreen, screen.LevelTimeScreen
from screen.MenuItems import Button, LevelButton, LevelTableCreator
from screen.BaseMenuScreen import BaseMenuScreen
from Resources import Resources

class LevelScreen(BaseMenuScreen):

    def __init__(self, game):
        super(LevelScreen, self).__init__(game)

        #levels
        self.mLevelTable = LevelTableCreator(self.modelsize, 4, self.countLevels(), lambda x: self.mGame.setScreen(screen.LevelTimeScreen.LevelTimeScreen(self.mGame, x)))
        self.mLevelTable.mLevelButtons.append(Button("back", 0.5, 8.5, b2Vec2(2,1), lambda: self.mGame.setScreen(screen.MenuScreen.MenuScreen(self.mGame))))

        #header
        self.title = self.titleFont.render("choose level", 0, (255,255,255))
        self.size = self.titleFont.size("choose level")
        self.titlepos = self.mCamera.getViewCoords(b2Vec2(self.modelsize.x / 2.0, self.modelsize.y / 6))

    def update(self, delta):
        BaseMenuScreen.update(self, delta)

    def render(self, delta):
        Pgl.app.surface.fill((67,80,129))
        Pgl.app.surface.blit(self.title, (self.titlepos.x - self.size[0] / 2.0, self.titlepos.y - self.size[1] / 2.0))

        btnToDraw = self.levelbutton
        for btn in self.mLevelTable.mLevelButtons:
            if isinstance(btn, Button):
                btnToDraw = self.menubutton
            viewpos = self.mCamera.getViewCoords(b2Vec2(btn.x, btn.y))
            btnToDraw.setSize(self.mCamera.getScaledSize(btn.size.x, btn.size.y))

            color = None
            if btn.mActive:
                btnToDraw.freeze(1, 0)
                color = (255,255,255)
            else:
                btnToDraw.freeze(0, 0)
                color = (141,60,1)

            btnToDraw.draw(delta, viewpos)

            #check if level is locked
            if isinstance(btn, LevelButton):
                if btn.mLocked:
                    lockpos = self.mCamera.getViewCoords(b2Vec2(btn.x + self.mLevelTable.mButtonSize.x / 1.5, btn.y + self.mLevelTable.mButtonSize.y / 1.5))
                    self.lock.draw(lockpos)

            btntxt = self.screenFont.render(str(btn.mText), 0, color)
            size = self.screenFont.size(str(btn.mText))
            txtpos = self.mCamera.getViewCoords(b2Vec2(btn.x + btn.size.x / 2 - (size[0] / self.mCamera.scale.x) / 2.0, btn.y + btn.size.y / 2 - (size[1] / self.mCamera.scale.y) / 2.0))
            Pgl.app.surface.blit(btntxt, (txtpos.x, txtpos.y))
            self.arrow.draw()

    def mouseClick(self, pos):
        mmp = self.mCamera.getModelCoords(b2Vec2(pos[0], pos[1]))

        for btn in self.mLevelTable.mLevelButtons:
            if btn.rect.collidepoint(mmp):
                btn.mAction()

    def mouseOver(self, pos):
        mmp = self.mCamera.getModelCoords(b2Vec2(pos[0], pos[1]))

        for btn in self.mLevelTable.mLevelButtons:
            btn.mActive = False
            if btn.rect.collidepoint(mmp):
                if isinstance(btn, LevelButton):
                    if btn.mLocked:
                        continue
                btn.mActive = True

    def keyInput(self, key):
        pass

    def countLevels(self):
        lvls = 0
        for filename in os.listdir(Resources.getInstance().resource_path("assets/levels")):
            if filename.endswith(".lvl"):
                lvls += 1

        return lvls
