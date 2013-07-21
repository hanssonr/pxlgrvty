from controller.MenuInput import MenuInput
from model.Camera import Camera
from libs.Pgl import *
from libs.Animation import Animation
from Resources import Resources
from Box2D import b2Vec2
from libs.RectF import RectF
import os, pygame, GameScreen

class LevelScreen(object):
    
    def __init__(self, game):
        pygame.mouse.set_visible(True)
        self.mGame = game
        self.mCamera = Camera(Pgl.width, Pgl.height)
        self.button = Animation(Resources.getInstance().mLevelButton, 2, 1, 0, self.mCamera.getScaledSize(1, 1))
        self.button.isLooping = False
        modelSize = self.mCamera.getModelCoords(b2Vec2(Pgl.width, Pgl.height))
        nrOfLvls = self.countLevels()
        self.mLevelTable = LevelTableCreator(modelSize, 4, nrOfLvls)
        game.setInput(MenuInput(self))
        
    def update(self, delta):
        pass 
    
    def render(self, delta):
        Pgl.app.surface.fill((167,74,20))
        
        for btn in self.mLevelTable.mLevelButtons:
            viewpos = self.mCamera.getViewCoords(b2Vec2(btn.x, btn.y))
            
            btntxt = Resources.getInstance().mFpsFont.render(str(btn.mText), 1, (255,255,255))
            size = Resources.getInstance().mFpsFont.size(str(btn.mText))
            txtpos = self.mCamera.getViewCoords(b2Vec2(btn.x + self.mLevelTable.mButtonSize.x / 2 - (size[0] / self.mCamera.scale.x) / 2.0, btn.y + self.mLevelTable.mButtonSize.y / 2 - (size[1] / self.mCamera.scale.y) / 2.0))
            
            self.button.setSize(self.mCamera.getScaledSize(self.mLevelTable.mButtonSize.x, self.mLevelTable.mButtonSize.y))
            if btn.mActive:
                self.button.freeze(1, 0)
            else:
                self.button.freeze(0, 0)
            self.button.draw(delta, viewpos)
            Pgl.app.surface.blit(btntxt, (txtpos.x, txtpos.y))

    def mouseClick(self, pos):
        mmp = self.mCamera.getModelCoords(b2Vec2(pos[0], pos[1]))
        
        for btn in self.mLevelTable.mLevelButtons:
            if btn.rect.collidepoint(mmp):
                self.mGame.setScreen(GameScreen.GameScreen(self.mGame, btn.mText))
                break
        
    def mouseOver(self, pos):
        mmp = self.mCamera.getModelCoords(b2Vec2(pos[0], pos[1]))
        
        for btn in self.mLevelTable.mLevelButtons:
            btn.mActive = False
            if btn.rect.collidepoint(mmp):
                btn.mActive = True
                
    def countLevels(self):
        lvls = 0
        for filename in os.listdir("assets/levels"):
            if filename.endswith(".lvl"):
                lvls += 1
                
        return lvls

class LevelTableCreator(object):
    mLevelButtons = []
    mButtonSize = b2Vec2(1,1)
    
    def __init__(self, modelsize, lvlPerColumn, nrOfLevels):
        self.mRows = max(1, nrOfLevels / lvlPerColumn)
        self.mCols = min(nrOfLevels, lvlPerColumn)
        width = self.mButtonSize.x * self.mCols
        height = self.mButtonSize.y * self.mRows
        count = 1
        for y in range(self.mRows):
            for x in range(self.mCols):
                mx = x * self.mButtonSize.x + modelsize.x / 2.0 - width / 2.0
                my = y * self.mButtonSize.y + modelsize.y / 2.0 - height / 2.0
                self.mLevelButtons.append(LevelButton(count, mx, my, self.mButtonSize))
                count += 1
        
    
class LevelButton(object):
    
    def __init__(self, text, x, y, size):
        self.mActive = False
        self.mText = text
        self.x, self.y = x, y
        self.rect = RectF(x, y, size.x, size.y)
        