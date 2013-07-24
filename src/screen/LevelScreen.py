from controller.MenuInput import MenuInput
from model.Camera import Camera
from libs.Pgl import *
from libs.Animation import Animation
from Resources import Resources
from Box2D import b2Vec2
from libs.RectF import RectF
from libs.Sprite import Sprite
import os, pygame, GameScreen, json, MenuScreen, LevelTimeScreen
from screen.MenuItems import Button, MenuAction

class LevelScreen(object):
    
    def __init__(self, game):
        pygame.mouse.set_visible(False)
        self.mGame = game
        self.mCamera = Camera(Pgl.width, Pgl.height)
        
        self.lock = Sprite(Resources.getInstance().mLock)
        self.lock.setSize(self.mCamera.getScaledSize((self.lock.getWidth()/float(self.lock.getHeight())) * 0.2, 0.2))
        
        self.arrow = Sprite(Resources.getInstance().mArrow) 
        self.arrow.setSize(self.mCamera.getScaledSize((self.arrow.getWidth()/float(self.arrow.getHeight())) * 0.5, 0.5))
        
        self.button = Animation(Resources.getInstance().mLevelButton, 2, 1, 0, self.mCamera.getScaledSize(1, 1), False)
        self.menubutton = Animation(Resources.getInstance().mMenuButton, 2, 1, 0, self.mCamera.getScaledSize(1, 1), False)
        
        self.modelsize = self.mCamera.getModelCoords(b2Vec2(Pgl.width, Pgl.height))
        
        nrOfLvls = self.countLevels()
        self.mLevelTable = LevelTableCreator(self.modelsize, 4, nrOfLvls)
        self.mLevelTable.mLevelButtons.append(Button("back", 0.5, 8.5, b2Vec2(2,1), MenuAction.BACK))
        
        self.screenFont = Resources.getInstance().getScaledFont(self.mCamera.scale.x / 3)
        self.titleFont = Resources.getInstance().getScaledFont(self.mCamera.scale.x * 2.0)
        
        self.mGame.input = MenuInput(self)
        
    def update(self, delta):
        pos = pygame.mouse.get_pos()
        self.arrow.setPosition(pos[0], pos[1])
        self.mouseOver(pos)
    
    def render(self, delta):
        #Pgl.app.surface.fill((167,74,20))
        Pgl.app.surface.fill((67,80,129))
        
        #header
        title = self.titleFont.render("choose level", 0, (255,255,255))
        size = self.titleFont.size("choose level")
        titlepos = self.mCamera.getViewCoords(b2Vec2(self.modelsize.x / 2.0, self.modelsize.y / 6))
        Pgl.app.surface.blit(title, (titlepos.x - size[0] / 2.0, titlepos.y - size[1] / 2.0))
        
        
        btnToDraw = self.button
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
                if isinstance(btn, LevelButton):
                    if not btn.mLocked:
                        self.mGame.setScreen(LevelTimeScreen.LevelTimeScreen(self.mGame, btn.mText))
                       #self.mGame.setScreen(GameScreen.GameScreen(self.mGame, btn.mText))
                elif isinstance(btn, Button):
                    if btn.mAction == MenuAction.BACK:
                        self.mGame.setScreen(MenuScreen.MenuScreen(self.mGame))
                break
        
    def mouseOver(self, pos):
        mmp = self.mCamera.getModelCoords(b2Vec2(pos[0], pos[1]))
        
        for btn in self.mLevelTable.mLevelButtons:
            btn.mActive = False
            if btn.rect.collidepoint(mmp):
                if isinstance(btn, LevelButton):
                    if btn.mLocked:
                        continue
                btn.mActive = True
                
    def countLevels(self):
        lvls = 0
        for filename in os.listdir("assets/levels"):
            if filename.endswith(".lvl"):
                lvls += 1
                
        return lvls

class LevelTableCreator(object):
    mLevelButtons = None
    mButtonSize = None
    
    def __init__(self, modelsize, lvlPerColumn, nrOfLevels):
        self.mLevelButtons = []
        self.mButtonSize = b2Vec2(1,1)
        lock = self.__readLevelLockState()
        self.mRows = max(1, nrOfLevels / lvlPerColumn)
        self.mCols = min(nrOfLevels, lvlPerColumn)
        width = self.mButtonSize.x * self.mCols
        height = self.mButtonSize.y * self.mRows
        count = 1
        for y in range(self.mRows):
            for x in range(self.mCols):
                mx = x * self.mButtonSize.x + modelsize.x / 2.0 - width / 2.0
                my = y * self.mButtonSize.y + modelsize.y / 2.0 - height / 2.0
                self.mLevelButtons.append(LevelButton(count, mx, my, self.mButtonSize, False if count <= int(lock) else True))
                count += 1
    
    """ 
    tries to open state file, if not exists or tampered with, create a new one 
    """
    def __readLevelLockState(self):
        lvldata = None
    
        try:
            with open("assets/state/state.json", "r") as state:
                lvldata = json.load(state)
                try:
                    return lvldata["LVL"]
                except:
                    raise IOError
        except (IOError):
            with open("assets/state/state.json", "w+") as state:
                json.dump({"LVL":"1"}, state)
                return 1       

class LevelButton(object):
    
    def __init__(self, text, x, y, size, locked):
        self.mLocked = locked
        self.mActive = False
        self.mText = text
        self.x, self.y = x, y
        self.size = size
        self.rect = RectF(x, y, size.x, size.y)
        